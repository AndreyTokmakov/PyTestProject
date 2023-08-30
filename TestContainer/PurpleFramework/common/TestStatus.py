import enum


class Status(enum.Enum):
    NotStarted = 0
    Running = 1
    Suspended = 2
    Completed = 3

    def __str__(self):
        return str(self.name)
