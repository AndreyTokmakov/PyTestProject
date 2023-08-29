
import enum


class TriggerType(enum.Enum):
    Manually = 0
    GitPoller = 1
    WebHook = 2
    Timer = 3

    def __str__(self):
        return str(self.name)
