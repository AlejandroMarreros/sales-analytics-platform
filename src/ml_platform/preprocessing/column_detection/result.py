from dataclasses import dataclass


@dataclass(frozen=True)
class ColumnMatch:
    column: object
    concept: str | None
    match_type: str
    confidence: str


@dataclass(frozen=True)
class ColumnDetectionResult:
    matches: tuple[ColumnMatch, ...]

    @property
    def valid(self) -> bool:
        return not any(match.match_type == "ambiguous" for match in self.matches)

    def get_match(self, column: object) -> ColumnMatch | None:
        for match in self.matches:
            if match.column == column:
                return match
        return None

    def get_concept(self, column: object) -> str | None:
        match = self.get_match(column)
        return None if match is None else match.concept

    def get_match_type(self, column: object) -> str | None:
        match = self.get_match(column)
        return None if match is None else match.match_type
