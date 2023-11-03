from dataclasses import dataclass


@dataclass
class Clamp:
    """Keep numbers within range."""

    minimum: int
    maximum: int

    @staticmethod
    def new(x: int, y: int) -> "Clamp":
        if x < y:
            return Clamp(x, y)
        return Clamp(y, x)

    def __call__(self, value: float) -> float:
        """Keep value within range."""
        if value < self.minimum:
            return self.minimum
        if value > self.maximum:
            return self.maximum
        return value

    def __str__(self) -> str:
        """As human readable string."""
        return f"Clamp({self.minimum}, {self.maximum})"
