from user_story import UserStory
import pythonic_md as md
import os, glob

_HARD_CODED_FILES_PATH = "./hard-coded-pages"

_REAL_REPO_NAMES = {
    'api-gateway': "API Gateway",
    'accounts-service': 'Accounts service',
    'mobile': 'Mobile',
    'noted': 'Misc',
    'notes-service': 'Note service',
    'recommendations-service': 'Recommendation service',
    'web-desktop': 'Web'
}

class PLD:
    before_user_stories: dict[str, str]
    user_stories: list[UserStory]
    rapports: list[str]

    def __init__(self, user_stories=list[UserStory]()):
        self.user_stories: list[UserStory] = user_stories
        self.before_user_stories = dict[str, str]()
        self.rapports = list[str]()

    def __read_whole_file(self, filename: str):
        try:
            content = ""
            with open(filename) as file:
                content = file.read()
            return content
        except Exception as e:
            print(e)
            return None

    def _generate_rapports(self):
        for filename in glob.glob(f"{_HARD_CODED_FILES_PATH}/rapports/*.md"):
            content = self.__read_whole_file(os.path.join(os.getcwd(), filename))
            self.rapports.append(content)

    def _generate_markdown_before_user_stories(self):
        self.before_user_stories["Description du document"] = self.__read_whole_file(
            f"{_HARD_CODED_FILES_PATH}/document-description.md"
        )
        self.before_user_stories["Tableau des révisions"] = self.__read_whole_file(
            f"{_HARD_CODED_FILES_PATH}/revision-table.md"
        )
        self.before_user_stories["Présentation du projet"] = self.__read_whole_file(
            f"{_HARD_CODED_FILES_PATH}/project-presentation.md"
        )
        self.before_user_stories["Schéma des livrables"] = self.__read_whole_file(
            f"{_HARD_CODED_FILES_PATH}/schemas.md"
        )

    def to_markdown(self, repo_name_in_order:list=[]):
        self._generate_markdown_before_user_stories()
        self._generate_rapports()

        output = ""
        for part in [
            "Description du document",
            "Tableau des révisions",
            "Présentation du projet",
            "Schéma des livrables",
        ]:
            output += f"{self.before_user_stories[part]}\n{md.separator()}\n"

        output += f"{md.title(md.bold('User stories'))}\n"
        index = 1
        last_repo_name = ""
        order_available = repo_name_in_order != []
        for story in self.user_stories:
            story_result = ""
            repo_name_index = 0
            if order_available:
                repo_name_index = repo_name_in_order.index(story.repo_name)
            if last_repo_name != story.repo_name:
                new_category_title = ""
                if order_available:
                        new_category_title += f"{repo_name_index + 1} - "  
                new_category_title += _REAL_REPO_NAMES[story.repo_name]
                output += md.title(md.bold(new_category_title), priority=2) + '\n'
                index = 1
            last_repo_name = story.repo_name
            if  order_available:
                story.title = f"{repo_name_index + 1}.{index} - " + story.title.strip()
            output += story.to_markdown()
            index += 1

        rapports_title = "Rapports d'avancement"
        output += f"\n{md.title(rapports_title, priority=1)}\n"  # chr(39) to workaround the apostrophe in a fstring
        output += f"\n{md.separator()}\n".join(self.rapports)
        return output
