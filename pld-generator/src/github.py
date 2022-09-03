import requests
import json
import os
import graphql
import logging
from user_story import Issue

# NOTE: Maybe use graphql framework

GITHUB_GRAPHQL_ENDPOINT = "https://api.github.com/graphql"
try:
    _GITHUB_AUTHENTIFICATION_HEADER = f"bearer {os.getenv('GITHUB_OAUTH_TOKEN')}"
except:
    logging.fatal("Please set the GITHUB_OAUTH_TOKEN variable")
MAX_ASSIGNEES=7
MAX_ISSUES=100
MAX_PROJECTS=5


def github_graphql_request(query):
    return graphql.request(GITHUB_GRAPHQL_ENDPOINT, query, headers={"authorization": _GITHUB_AUTHENTIFICATION_HEADER})    

def get_project_id(org_name, project_name):
    query = """query{
      organization(login: \"""" + org_name + """\") {
        projectsV2(first: \"""" + MAX_PROJECTS + """\") {
          nodes {
            id
            title
          }
        }
      }
    }"""
    req_json = github_graphql_request(query)

    try:
        projects = req_json["data"]["organization"]["projectsV2"]["nodes"]
        project_obj = next(filter(lambda element: element["title"] == project_name, projects))
        return project_obj["id"]
    except:
        return None

def make_issue(json_issue):
    result = Issue()
    json_issue = json_issue["content"]
    result.title = json_issue["title"]
    result.body = json_issue["body"]
    result.assignees = [element["login"] for element in json_issue["assignees"]["nodes"]]
    result.repo_name = json_issue["repository"]["name"]

def get_all_issues_from_project(project_id):
    query = """{
      node(id: \"""" + project_id + """\") {
        ... on ProjectV2 {
          items(first: """ + MAX_ISSUES + """, after: null) {
            nodes {
              content {
                ... on Issue {
                  title
                  body
                  assignees(first: """ + MAX_ASSIGNEES + """) {
                    nodes {
                      login
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
    req_json = github_graphql_request(query)

    try:
        all_issues_json = req_json["data"]["node"]["items"]["nodes"]
        all_issues_obj  = [make_issue(json) for json in all_issues_json]
        return all_issues_obj
    except:
        return None
