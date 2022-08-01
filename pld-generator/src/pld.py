from user_story import UserStory

class PLD:
    def __init__(self):
        self.user_stories = list[UserStory]

    def to_markdown(self):
        output =  ""
        output += ''.join([story.to_markdown() for story in self.user_stories])
        return output
