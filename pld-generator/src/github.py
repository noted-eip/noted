import requests
import json
import os
import graphql
import logging
from user_story import Issue

# NOTE: Maybe use graphql framework later

GITHUB_REST_ENDPOINT    =  'https://api.github.com'
GITHUB_GRAPHQL_ENDPOINT = f"{GITHUB_REST_ENDPOINT}/graphql"
try:
    _GITHUB_AUTHENTIFICATION_HEADER = f"bearer {os.getenv('GITHUB_OAUTH_TOKEN')}"
except:
    logging.fatal("Please set the GITHUB_OAUTH_TOKEN variable")

MAX_ASSIGNEES = int(os.getenv("MAX_ASSIGNEES") or 7) 
MAX_ISSUES    = int(os.getenv("MAX_ISSUES")    or 100)    
MAX_PROJECTS  = int(os.getenv("MAX_PROJECTS")  or 5)  


def github_graphql_request(query:str):
    return graphql.request(GITHUB_GRAPHQL_ENDPOINT, query, headers={"authorization": _GITHUB_AUTHENTIFICATION_HEADER})    

def get_project_id(org_name:str, project_name:str):
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
    req_json = github_graphql_request(query)

    try:
        projects = req_json["data"]["organization"]["projectsV2"]["nodes"]
        project_obj = next(filter(lambda element: element["title"] == project_name, projects))
        return project_obj["id"]
    except:
        return None

def _make_issue_from_github_graphl_result(json_issue:dict[str, any]):
    result = Issue()
    json_issue = json_issue["content"]
    result.title = json_issue["title"]
    result.body = json_issue["body"]
    result.assignees = [element["login"] for element in json_issue["assignees"]["nodes"]]
    result.repo_name = json_issue["repository"]["name"]
    return result

def get_name_from_username(username:str):
    pass    

def get_all_issues_from_project(project_id:str):
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
        all_issues_obj  = [_make_issue_from_github_graphl_result(json) for json in all_issues_json]
        return all_issues_obj
    except:
        return None
