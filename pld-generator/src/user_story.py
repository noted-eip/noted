from typing import Optional
from decorators import object_must_be_valid
import inspect

class UserStory:
    title:               Optional[str]
    description:         Optional[str]
    assignees:           Optional[list[str]]
    definitions_of_done: Optional[list[str]]
    duration_in_days:    Optional[float]

    def is_valid(self) -> bool:
        return len(self.__dict__) == len(inspect.get_annotations(UserStory))

    @object_must_be_valid
    def to_markdown(self) -> str:
        pass
