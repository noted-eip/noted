from user_story import UserStory
import md


class PLD:
    def __init__(self, user_stories=list[UserStory]()):
        self.user_stories: list[UserStory] = user_stories

    def to_markdown(self):
        # TODO : All the other informations
        output = ""
        output += f"\n{md.separator()}\n".join(
            [story.to_markdown() for story in self.user_stories]
        )
        return output
