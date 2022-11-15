from typing import Optional
from decorators import object_must_be_valid
import inspect
import pythonic_md as md
import re
import logging


class UserStory:
    title: Optional[str]
    description: Optional[str]
    assignees: Optional[list[str]]
    definitions_of_done: Optional[list[str]]
    duration_in_days: Optional[str]

    repo_name: Optional[str]

    def __str__(self):
        return f"{self.__dict__}"

    def is_valid(self) -> bool:
        return len(self.__dict__) == len(inspect.get_annotations(UserStory))

    @object_must_be_valid
    def to_markdown(self) -> str:
        result = "\n".join(
            [
                md.title(md.bold(self.title), priority=2),
                md.title("Description", priority=3),
                self.description,
                md.title("Definitions Of Done", priority=3),
                "\n".join(self.definitions_of_done),
                "\n",
                f"<b>{self.duration_in_days} JH - {', '.join(self.assignees)}</b>",
                "\n",
            ]
        )
        if result is None:
            logging.error(f"'{self.title}' user story is not valid.")
        return result


class Issue:
    title: str
    body: str
    assignees: list[str]
    repo_name: str

    def __str__(self):
        return f"{self.__dict__}"

    # NOTE: idk maybe below methods belong elsewhere

    def _clean_empty_list_elements(self, lst: list):
        return list(filter(None, lst))

    def _parse_issue_body_to_dict(self, body: str):
        clean = self._clean_empty_list_elements

        body_splitted_by_blocks_dirty = body.split(md.title("", priority=3))
        body_splitted_by_blocks = clean(body_splitted_by_blocks_dirty)

        block_dictionnary = dict[str, str]()

        for block in body_splitted_by_blocks:
            tuppled_block = tuple(block.split("\n", maxsplit=1))

            block_title = tuppled_block[0].strip()
            block_content = tuppled_block[1]

            block_dictionnary[block_title] = block_content.strip()
        return block_dictionnary

    def _clean_crlf_to_lf(self, text: str):
        text = text.replace("\r\n\r\n", "\n", -1)
        text = text.replace("\r\n", "\n", -1)
        return text.replace("\n\n", "\n", -1)

    def _clean_html_comments(self, text: str):
        return re.sub("(<!--.*?-->)", "", text, flags=re.DOTALL)

    def to_user_story(self):
        result = UserStory()
        result.title = self.title
        result.assignees = self.assignees
        result.repo_name = self.repo_name

        self.body = self._clean_html_comments(self.body)
        self.body = self._clean_crlf_to_lf(self.body).strip("\n ")
        body_dict = self._parse_issue_body_to_dict(self.body)

        try:
            result.definitions_of_done = body_dict["Definition of Done"].split("\n")
            result.description = body_dict["Description"]
            duration_regex = re.search("\d+([.,]\d+)?", body_dict["Estimation"])
            if duration_regex:
                duration_fix = duration_regex.group().replace(",", ".")
                result.duration_in_days = duration_fix
            else:
                result.duration_in_days = "X"

        except Exception as e:
            logging.error(f"error with issue '{result.title}': {e}\n")
        return result
