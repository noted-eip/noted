from typing import Optional
from decorators import object_must_be_valid
import inspect
import markdown as md

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
        return '\n'.join([
            md.title(self.title, priority=2),
            md.title("Assignees", priority=3),
            md.dotted_list(self.definitions_of_done),
            md.title("DOD", priority=3),
            md.dotted_list(self.definitions_of_done),
            md.title(f"{self.duration_in_days} {md.bold('j/H')}", priority=4)
        ])
