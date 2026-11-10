"""Pydantic models for exercise sheets, exercises and query results."""

import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Exercise(BaseModel):
    id: str  # e.g. "0.3"; must start with the sheet number
    section: str  # heading the exercise is grouped under, e.g. "Filtern"
    title: str
    task: str
    hint: str = ""
    solution: str
    ordered: bool = False  # does row order matter?


class Sheet(BaseModel):
    """One exercise sheet (one 90-minute session) working on a single database."""

    model_config = ConfigDict(populate_by_name=True)

    number: int
    title: str
    db: str
    goal: str
    exercises: list[Exercise] = Field(alias="exercise")

    @model_validator(mode="after")
    def _ids_match_number(self) -> "Sheet":
        for exercise in self.exercises:
            if not exercise.id.startswith(f"{self.number}."):
                raise ValueError(f"exercise {exercise.id} does not belong to sheet {self.number}")
        return self


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


def load_sheets(directory: Path) -> list[Sheet]:
    """Load all `*.toml` sheets from `directory`, ordered by sheet number."""
    sheets = [
        Sheet(**tomllib.loads(file.read_text(encoding="utf-8")))
        for file in sorted(directory.glob("*.toml"))
    ]
    sheets.sort(key=lambda s: s.number)
    ids = [e.id for s in sheets for e in s.exercises]
    if len(ids) != len(set(ids)):
        raise ValueError("exercise ids must be unique")
    return sheets


def find_exercise(sheets: list[Sheet], exercise_id: str) -> tuple[Sheet, Exercise] | None:
    for sheet in sheets:
        for exercise in sheet.exercises:
            if exercise.id == exercise_id:
                return sheet, exercise
    return None
