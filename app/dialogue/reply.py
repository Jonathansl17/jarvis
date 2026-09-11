"""The outcome of one coordinated user turn."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AssistantReply:
    """What the assistant says back, and whether it is still waiting on data."""

    text: str
    awaiting_field: bool
    model_name: str | None
