from user_story import UserStory
import md

class PLD:
    def __init__(self):
        self.user_stories = list[UserStory]

    def to_markdown(self):
        # TODO : All the other informations
        output =  ""
        output += md.separator().join([story.to_markdown() for story in self.user_stories])
        return output
