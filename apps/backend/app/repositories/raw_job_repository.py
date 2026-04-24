from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.models.raw_job import RawJob


class RawJobRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, raw_job_id: int) -> RawJob | None:
        stmt = select(RawJob).where(RawJob.id == raw_job_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_content_hash(self, content_hash: str) -> RawJob | None:
        stmt = select(RawJob).where(RawJob.content_hash == content_hash)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, *, raw_text: str, source: str, content_hash: str) -> RawJob:
        raw_job = RawJob(
            raw_text=raw_text,
            source=source,
            content_hash=content_hash,
        )
        self.db.add(raw_job)
        self.db.commit()
        self.db.refresh(raw_job)
        return raw_job

    def list(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[RawJob], int]:
        sortable_columns = {
            "id": RawJob.id,
            "created_at": RawJob.created_at,
            "source": RawJob.source,
        }
        sort_column = sortable_columns.get(sort_by, RawJob.created_at)

        if sort_order.lower() == "asc":
            order_clause = sort_column.asc()
        else:
            order_clause = sort_column.desc()

        stmt: Select[tuple[RawJob]] = (
            select(RawJob)
            .order_by(order_clause)
            .offset(offset)
            .limit(limit)
        )
        items = list(self.db.execute(stmt).scalars().all())

        total_stmt = select(func.count()).select_from(RawJob)
        total = self.db.execute(total_stmt).scalar_one()

        return items, total