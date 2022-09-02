import requests
import json

GITHUB_GRAPHQL_ENDPOINT = "https://api.github.com/graphql"

def graphql_request(endpoint, query):
    try:
        req = requests.post(endpoint, json={"query": query})
        return req.json()
    except Exception as e:
        print("Error: {e}")
        return None

def get_project_id(org_name, project_name):
    query = """query{
      organization(login: \"""" + org_name + """\") {
        projectsNext(first: 20) {
          nodes {
            id
            title
          }
        }
      }
    }"""
    req_json = graphql_request(GITHUB_GRAPHQL_ENDPOINT, query)
    
    projects = req_json["data"]["organization"]["projectsNext"]["nodes"]
    
    try:
        project_obj = next(filter(projects, lambda element: element["title"] == project_name))
        return project_obj["id"]
    except StopIteration:
        return None
