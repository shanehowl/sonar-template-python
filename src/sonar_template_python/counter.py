class Counter:
    """A counter that can be incremented, decremented and reset to its initial value."""

    def __init__(self, initial: int = 0) -> None:
        self.initial = initial
        self.count = initial

    def increment(self) -> int:
        self.count += 1
        return self.count

    def decrement(self) -> int:
        self.count -= 1
        return self.count

    def reset(self) -> int:
        self.count = self.initial
        return self.count
