import github
import pld

GITHUB_ORG_NAME     = os.getenv('GITHUB_ORG_NAME')     or 'noted-eip'
GITHUN_PROJECT_NAME = os.getenv('GITHUB_PROJECT_NAME') or 'Roadmap'

def generate() -> None:
    project_id = github.get_project_id(GITHUB_ORG_NAME, GITHUB_PROJECT_NAME)

    issues_object_list = github.get_all_issues_from_project(id)
