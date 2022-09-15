import github
import os
from pld import PLD

GITHUB_ORG_NAME = os.getenv("GITHUB_ORG_NAME") or "noted-eip"
GITHUB_PROJECT_NAME = os.getenv("GITHUB_PROJECT_NAME") or "Roadmap"


def generate() -> None:

    project_id = github.get_project_id(GITHUB_ORG_NAME, GITHUB_PROJECT_NAME)

    issues_object_list = github.get_all_issues_from_project(project_id)

    user_stories = [issue.to_user_story() for issue in issues_object_list]

    user_stories = sorted(user_stories, key=lambda story: story.repo_name)

    pld = PLD(user_stories)

    # NOTE : Placeholder
    print(pld.to_markdown())
