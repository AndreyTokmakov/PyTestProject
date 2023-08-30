import enum


class CompletionStatus(enum.Enum):
    Passed = 0
    Warning = 1
    Failed = 2

    def __str__(self):
        return str(self.name)
