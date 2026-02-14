from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

ActionStatus = Literal["moved", "skipped", "error"]


@dataclass(slots=True)
class MoveAction:
    source: Path
    destination: Path
    category: str
    status: ActionStatus
    message: str | None = None


@dataclass(slots=True)
class RunReport:
    total_scanned: int = 0
    total_moved: int = 0
    total_skipped: int = 0
    total_errors: int = 0
    actions: list[MoveAction] = field(default_factory=list)

    def add_action(self, action: MoveAction) -> None:
        self.actions.append(action)
        self.total_scanned += 1
        if action.status == "moved":
            self.total_moved += 1
        elif action.status == "skipped":
            self.total_skipped += 1
        elif action.status == "error":
            self.total_errors += 1
