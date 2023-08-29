from enum import Enum, auto


class Category(Enum):
    Regression = auto()
    Performance = auto()
    Security = auto()
    Scheduled = auto()
    All = auto()  # selection for all categories

    @staticmethod
    def from_str(text):
        if text is None:
            return None
        categories = [category for category in dir(Category) if not category.startswith('_')]
        for category in categories:
            if text.startswith(category):
                return getattr(Category, category)
        return None

    def __str__(self):
        return str(self.name)
