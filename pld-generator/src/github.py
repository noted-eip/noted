import requests
import json
import os
import graphql
import logging
from user_story import Issue

# NOTE: Maybe use graphql framework later

GITHUB_REST_ENDPOINT = "https://api.github.com"
GITHUB_GRAPHQL_ENDPOINT = f"{GITHUB_REST_ENDPOINT}/graphql"
try:
    token = os.getenv("GITHUB_OAUTH_TOKEN")
    assert token is not None
    _GITHUB_AUTHENTIFICATION_HEADER = f"bearer {token}"
except:
    import sys

    logging.fatal("Please set the GITHUB_OAUTH_TOKEN variable")
    sys.exit(1)

MAX_ASSIGNEES = int(os.getenv("MAX_ASSIGNEES") or 7)
MAX_LABELS = int(os.getenv("MAX_LABELS") or 7)
MAX_ISSUES = int(os.getenv("MAX_ISSUES") or 100)
MAX_PROJECTS = int(os.getenv("MAX_PROJECTS") or 5)

username_to_name: dict[str, str] = {
    "kfleury": "Killian Fleury",
    "tomasit": "Thomas Ittel",
}


def github_graphql_request(query: str):
    return graphql.request(
        GITHUB_GRAPHQL_ENDPOINT,
        query,
        headers={"authorization": _GITHUB_AUTHENTIFICATION_HEADER},
    )


def github_rest_request(endpoint: str, params=None):
    return requests.get(
        f"{GITHUB_REST_ENDPOINT}{endpoint}",
        params=params,
        headers={"authorization": _GITHUB_AUTHENTIFICATION_HEADER},
    )


def get_project_id(org_name: str, project_name: str):
    # fmt: off
    query = """query{
      organization(login: \"""" + org_name + """\") {
        projectsV2(first: """ + str(MAX_PROJECTS) + """) {
          nodes {
            id
            title
          }
        }
      }
    }"""
    # fmt: on
    req_json = github_graphql_request(query)

    try:
        projects = req_json["data"]["organization"]["projectsV2"]["nodes"]
        project_obj = next(
            filter(lambda element: element["title"] == project_name, projects)
        )
        return project_obj["id"]
    except:
        return None


def _make_issue_from_github_graphl_result(json_issue: dict[str, any]):
    result = Issue()
    json_issue = json_issue["content"]
    result.title = json_issue["title"]
    result.body = json_issue["body"]

    result.assignees = []

    global username_to_name
    for element in json_issue["assignees"]["nodes"]:
        username = element["login"]
        if username not in username_to_name:
            username_to_name[username] = get_name_from_username(username)
            if username_to_name[username] is None:  # NOTE : Placeholder
                username_to_name[username] = username
        result.assignees.append(username_to_name[username])

    result.repo_name = json_issue["repository"]["name"]
    return result


def get_name_from_username(username: str):
    try:
        result = github_rest_request(f"/users/{username}")
        return result.json()["name"]
    except:
        return None


def get_all_issues_from_project(project_id: str):
    # fmt: off
    query = """{
      node(id: \"""" + project_id + """\") {
        ... on ProjectV2 {
          items(first: """ + str(MAX_ISSUES) + """, after: null) {
            nodes {
              content {
                ... on Issue {
                  title
                  body
                  assignees(first: """ + str(MAX_ASSIGNEES) + """) {
                    nodes {
                      login
                    }
                  }
                  labels(first: """ + str(MAX_LABELS) + """) {
                    nodes {
                      name
                    }
                  }
                  repository {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }"""
    # fmt: on
    req_json = github_graphql_request(query)

    try:
        all_issues_json = req_json["data"]["node"]["items"]["nodes"]

        check_if_issue_is_a_user_story = (
            lambda issue: {"name": "noted/story"} in issue["content"]["labels"]["nodes"]
        )

        all_issues_json = list(filter(check_if_issue_is_a_user_story, all_issues_json))

        all_issues_obj = [
            _make_issue_from_github_graphl_result(json) for json in all_issues_json
        ]

        return all_issues_obj
    except Exception as e:
        logging.error(e)
        return None
