"""Pydantic models for exercises and query results."""

import tomllib
from pathlib import Path

from pydantic import BaseModel, Field


class Exercise(BaseModel):
    id: str  # e.g. "0.3"
    lesson: int
    title: str
    db: str
    task: str
    hint: str = ""
    solution: str
    ordered: bool = False  # does row order matter?


class QueryResult(BaseModel):
    columns: list[str] = Field(default_factory=list)
    rows: list[list[str | int | float | None]] = Field(default_factory=list)
    truncated: bool = False
    error: str = ""
    rowcount: int = -1  # affected rows for writes


class CheckResult(BaseModel):
    ok: bool
    message: str
    result: QueryResult | None = None


def load_exercises(directory: Path) -> list[Exercise]:
    exercises: list[Exercise] = []
    for file in sorted(directory.glob("*.toml")):
        data = tomllib.loads(file.read_text(encoding="utf-8"))
        exercises.extend(Exercise(**item) for item in data["exercise"])
    return exercises
