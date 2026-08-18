"""Thread-safe status journal for parametric studies."""

from __future__ import annotations

import json
import threading
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

CaseStatus = Literal["pending", "running", "solved", "error"]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class SweepCaseRecord:
    """Timing and outcome of one sweep point."""

    index: int
    name: str
    parameters: dict[str, Any]
    status: CaseStatus = "pending"
    started_at: str | None = None
    finished_at: str | None = None
    duration_seconds: float | None = None
    error: str | None = None


class SweepJournal:
    """Keep in-memory statuses and optionally persist every transition to JSON."""

    def __init__(self, records: list[SweepCaseRecord], path: str | Path | None = None):
        self.path = None if path is None else Path(path).expanduser().resolve()
        self.started_at = _now()
        self.finished_at: str | None = None
        self.records = {record.index: record for record in records}
        self.events: list[dict[str, Any]] = []
        self._started_monotonic: dict[int, float] = {}
        self._lock = threading.RLock()
        self._write()

    def start(self, index: int, monotonic_time: float) -> None:
        with self._lock:
            record = self.records[index]
            record.status = "running"
            record.started_at = _now()
            self._started_monotonic[index] = monotonic_time
            self._event(record, "running")

    def finish(
        self,
        index: int,
        status: Literal["solved", "error"],
        monotonic_time: float,
        error: str | None = None,
    ) -> None:
        with self._lock:
            record = self.records[index]
            record.status = status
            record.finished_at = _now()
            started = self._started_monotonic.pop(index, monotonic_time)
            record.duration_seconds = round(max(0.0, monotonic_time - started), 6)
            record.error = error
            self._event(record, status)

    def close(self) -> None:
        with self._lock:
            self.finished_at = _now()
            self._write()

    @property
    def summary(self) -> dict[str, int]:
        counts = {"pending": 0, "running": 0, "solved": 0, "error": 0}
        for record in self.records.values():
            counts[record.status] += 1
        return counts

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "summary": self.summary,
            "cases": [asdict(self.records[index]) for index in sorted(self.records)],
            "events": list(self.events),
        }

    def _event(self, record: SweepCaseRecord, status: CaseStatus) -> None:
        self.events.append(
            {
                "timestamp": _now(),
                "index": record.index,
                "name": record.name,
                "status": status,
                "error": record.error,
            }
        )
        self._write()

    def _write(self) -> None:
        if self.path is None:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2, default=str) + "\n",
            encoding="utf-8",
        )
        temporary.replace(self.path)


__all__ = ["CaseStatus", "SweepCaseRecord", "SweepJournal"]
