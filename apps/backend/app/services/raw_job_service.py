import hashlib

from app.models.raw_job import RawJob
from app.repositories.raw_job_repository import RawJobRepository


class RawJobService:
    def __init__(self, repository: RawJobRepository) -> None:
        self.repository = repository

    @staticmethod
    def generate_content_hash(raw_text: str) -> str:
        normalized_text = " ".join(raw_text.split()).strip().lower()
        return hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()

    def create_raw_job(self, *, raw_text: str, source: str) -> tuple[RawJob, bool]:
        content_hash = self.generate_content_hash(raw_text)
        existing = self.repository.get_by_content_hash(content_hash)

        if existing is not None:
            return existing, False

        created = self.repository.create(
            raw_text=raw_text,
            source=source,
            content_hash=content_hash,
        )
        return created, True

    def get_raw_job(self, raw_job_id: int) -> RawJob | None:
        return self.repository.get_by_id(raw_job_id)

    def list_raw_jobs(
        self,
        *,
        limit: int,
        offset: int,
        sort_by: str,
        sort_order: str,
    ) -> tuple[list[RawJob], int]:
        return self.repository.list(
            limit=limit,
            offset=offset,
            sort_by=sort_by,
            sort_order=sort_order,
        )