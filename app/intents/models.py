"""The data shapes a parse produces, framework-free."""

from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True)
class Turn:
    """One utterance in a conversation, spoken or typed."""

    speaker: Literal["user", "assistant"]
    text: str


@dataclass(frozen=True)
class ResolvedIntent:
    """A fully identified model call: every required field is present."""

    model_name: str
    fields: dict[str, Any]


@dataclass(frozen=True)
class NeedsInput:
    """A partially identified model call, still missing some fields."""

    model_name: str
    fields: dict[str, Any]
    missing: list[str]


ParseResult = ResolvedIntent | NeedsInput

# The shape of an intent a `Conversation` keeps waiting on further input for
# is identical to `NeedsInput` — reused rather than duplicated.
PendingIntent = NeedsInput
