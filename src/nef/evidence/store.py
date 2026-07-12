"""Write-once canonical evidence storage and offline verification."""

from __future__ import annotations

import json
import os
import re
import stat
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from pydantic import ValidationError

from nef.contracts import (
    EvidenceManifest,
    EvidenceObject,
    canonical_json_bytes,
    canonical_sha256,
)

RETENTION_DAYS = 400
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_FORBIDDEN_KEYS = re.compile(
    r"(?:^|_)(?:api_key|github_token|password|private_key|secret_key|signing_seed|token)$",
    re.IGNORECASE,
)
_SECRET_TEXT = re.compile(r"-{5}BEGIN [A-Z0-9 ]*PRIVATE KEY-{5}|gh[pousr]_[A-Za-z0-9]{20,}")


class EvidenceError(ValueError):
    """Base error for evidence that cannot be safely stored or verified."""


class EvidenceIntegrityError(EvidenceError):
    """Stored evidence is missing, malformed, non-canonical, or inconsistent."""


class EvidenceConflictError(EvidenceError):
    """A write-once address already contains different bytes."""


class SensitiveEvidenceError(EvidenceError):
    """Evidence contains material matching a detectable forbidden pattern."""


class RetentionSetupError(EvidenceError):
    """The required retention policy was not verified as available."""


@dataclass(frozen=True)
class RetentionMetadata:
    """Honest retention intent; this is not a permanence guarantee."""

    requested_days: int
    observed_maximum_days: int
    assurance: str = "policy-intent-not-permanence"

    def as_json(self) -> dict[str, object]:
        return {
            "assurance": self.assurance,
            "observed_maximum_days": self.observed_maximum_days,
            "requested_days": self.requested_days,
        }


@dataclass(frozen=True)
class VerifiedEvidence:
    """A sealed manifest whose canonical objects and retention record were verified."""

    manifest: EvidenceManifest
    manifest_digest: str
    object_count: int
    retention: RetentionMetadata

    def summary(self) -> dict[str, object]:
        return {
            "manifest_digest": self.manifest_digest,
            "object_count": self.object_count,
            "retention": self.retention.as_json(),
            "verified": True,
        }


class EvidenceStore:
    """Local write-once store for canonical JSON evidence bundles."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()

    def put_json(self, logical_path: str, value: object) -> EvidenceObject:
        """Store one canonical JSON value and return its manifest entry."""
        encoded = canonical_json_bytes(value)
        digest = canonical_sha256(value)
        evidence = EvidenceObject(
            path=logical_path,
            media_type="application/json",
            size_bytes=len(encoded),
            sha256=digest,
        )
        canonical_value = self._parse_json(encoded, Path(evidence.path))
        _refuse_sensitive(evidence.path, canonical_value)
        self._create_without_overwrite(self._blob_path(digest), encoded)
        return evidence

    def seal(
        self,
        manifest: EvidenceManifest,
        *,
        maximum_retention_days: int | None,
    ) -> VerifiedEvidence:
        """Validate all objects and publish retention metadata then manifest."""
        retention = self._retention(maximum_retention_days)
        self._verify_manifest_objects(manifest)
        digest = canonical_sha256(manifest)
        retention_record = {
            "manifest_digest": digest,
            **retention.as_json(),
        }
        self._create_without_overwrite(
            self._retention_path(digest), canonical_json_bytes(retention_record)
        )
        self._create_without_overwrite(self._manifest_path(digest), canonical_json_bytes(manifest))
        return self.verify(digest)

    def verify(self, manifest_digest: str) -> VerifiedEvidence:
        """Verify a sealed bundle offline without executing evidence or target code."""
        self._validate_digest(manifest_digest)
        try:
            manifest_value = self._read_canonical(
                self._manifest_path(manifest_digest), manifest_digest
            )
            if not isinstance(manifest_value, Mapping):
                raise EvidenceIntegrityError("manifest must be a JSON object")
            manifest = EvidenceManifest.model_validate(manifest_value)
        except (EvidenceIntegrityError, ValidationError) as exc:
            raise EvidenceIntegrityError(f"manifest verification failed: {exc}") from exc

        self._verify_manifest_objects(manifest)
        retention = self._read_retention(manifest_digest)
        return VerifiedEvidence(
            manifest=manifest,
            manifest_digest=manifest_digest,
            object_count=len(manifest.objects),
            retention=retention,
        )

    def _verify_manifest_objects(self, manifest: EvidenceManifest) -> None:
        for evidence in manifest.objects:
            if evidence.media_type != "application/json":
                raise EvidenceIntegrityError(
                    f"unsupported evidence media type for {evidence.path}: {evidence.media_type}"
                )
            value = self._read_canonical(
                self._blob_path(evidence.sha256),
                evidence.sha256,
                logical_path=evidence.path,
            )
            if len(canonical_json_bytes(value)) != evidence.size_bytes:
                raise EvidenceIntegrityError(f"size mismatch for evidence object {evidence.path}")

    def _read_retention(self, manifest_digest: str) -> RetentionMetadata:
        path = self._retention_path(manifest_digest)
        value = self._read_canonical(path, None)
        if not isinstance(value, Mapping):
            raise EvidenceIntegrityError("retention metadata must be a JSON object")
        expected_keys = {
            "assurance",
            "manifest_digest",
            "observed_maximum_days",
            "requested_days",
        }
        if set(value) != expected_keys or value.get("manifest_digest") != manifest_digest:
            raise EvidenceIntegrityError("retention metadata does not match the sealed manifest")
        requested = value.get("requested_days")
        observed = value.get("observed_maximum_days")
        assurance = value.get("assurance")
        valid_types = (
            type(requested) is int and type(observed) is int and isinstance(assurance, str)
        )
        if not valid_types:
            raise EvidenceIntegrityError("retention metadata has invalid field types")
        requested_days = cast(int, requested)
        observed_days = cast(int, observed)
        assurance_text = cast(str, assurance)
        if requested_days != RETENTION_DAYS or observed_days < RETENTION_DAYS:
            raise EvidenceIntegrityError("retention metadata does not satisfy 400-day policy")
        if assurance_text != "policy-intent-not-permanence":
            raise EvidenceIntegrityError("retention metadata overstates its assurance")
        return RetentionMetadata(requested_days, observed_days, assurance_text)

    @staticmethod
    def _retention(maximum: int | None) -> RetentionMetadata:
        if maximum is None or type(maximum) is not int or maximum < RETENTION_DAYS:
            raise RetentionSetupError(
                "400-day retention must be observed as supported before sealing"
            )
        return RetentionMetadata(RETENTION_DAYS, maximum)

    def _read_canonical(
        self,
        path: Path,
        expected_digest: str | None,
        *,
        logical_path: str | None = None,
    ) -> object:
        encoded = self._read_regular(path)
        value = self._parse_json(encoded, path)
        try:
            canonical = canonical_json_bytes(value)
        except TypeError as exc:
            raise EvidenceIntegrityError(f"invalid canonical JSON at {path}: {exc}") from exc
        if encoded != canonical:
            raise EvidenceIntegrityError(f"evidence is not canonical JSON at {path}")
        if logical_path is not None:
            _refuse_sensitive(logical_path, value)
        if expected_digest is not None and canonical_sha256(value) != expected_digest:
            raise EvidenceIntegrityError(f"digest mismatch at {path}")
        return value

    @staticmethod
    def _parse_json(encoded: bytes, path: Path) -> object:
        try:
            return json.loads(encoded.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise EvidenceIntegrityError(f"malformed JSON at {path}: {exc}") from exc

    @staticmethod
    def _read_regular(path: Path) -> bytes:
        try:
            mode = path.lstat().st_mode
        except FileNotFoundError as exc:
            raise EvidenceIntegrityError(f"missing evidence file: {path}") from exc
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            raise EvidenceIntegrityError(f"evidence path is not a regular file: {path}")
        try:
            return path.read_bytes()
        except OSError as exc:
            raise EvidenceIntegrityError(f"cannot read evidence file {path}: {exc}") from exc

    def _create_without_overwrite(self, path: Path, encoded: bytes) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=".nef-stage-", dir=path.parent)
        temporary = Path(temporary_name)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(encoded)
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary, path, follow_symlinks=False)
            except FileExistsError as exc:
                if self._read_regular(path) != encoded:
                    raise EvidenceConflictError(
                        f"write-once path already contains different bytes: {path}"
                    ) from exc
            self._fsync_directory(path.parent)
        except EvidenceError:
            raise
        except OSError as exc:
            raise EvidenceIntegrityError(f"atomic evidence publication failed: {exc}") from exc
        finally:
            temporary.unlink(missing_ok=True)

    @staticmethod
    def _fsync_directory(directory: Path) -> None:
        descriptor = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def _blob_path(self, digest: str) -> Path:
        self._validate_digest(digest)
        return self.root / "evidence/v1/blobs/sha256" / digest[:2] / f"{digest}.json"

    def _manifest_path(self, digest: str) -> Path:
        self._validate_digest(digest)
        return self.root / "evidence/v1/manifests/sha256" / digest[:2] / f"{digest}.json"

    def _retention_path(self, digest: str) -> Path:
        self._validate_digest(digest)
        return self.root / "evidence/v1/bundles" / digest / "retention.json"

    @staticmethod
    def _validate_digest(digest: str) -> None:
        if not _DIGEST.fullmatch(digest):
            raise EvidenceIntegrityError("evidence digest must be lowercase SHA-256")


def _refuse_sensitive(logical_path: str, value: object) -> None:
    parts = {part.lower() for part in Path(logical_path).parts}
    forbidden_path = any(
        part == ".env"
        or part.startswith(".env.")
        or part in {"credential", "credentials", "secret", "secrets"}
        or part.startswith(("credential.", "credentials.", "secret.", "secrets."))
        for part in parts
    )
    if forbidden_path:
        raise SensitiveEvidenceError(f"forbidden evidence path: {logical_path}")
    _scan_value(value, path=logical_path)


def _scan_value(value: object, *, path: str) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            if _FORBIDDEN_KEYS.search(key_text):
                raise SensitiveEvidenceError(f"detectable sensitive field at {path}.{key_text}")
            _scan_value(item, path=f"{path}.{key_text}")
    elif isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        for index, item in enumerate(value):
            _scan_value(item, path=f"{path}[{index}]")
    elif isinstance(value, str) and _SECRET_TEXT.search(value):
        raise SensitiveEvidenceError(f"detectable secret material at {path}")
