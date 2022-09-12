import requests

def request(endpoint:str, query:str, headers:dict[str, str] = None):
    try:
        req = requests.post(
          endpoint, 
          json={"query": query}, 
          headers=headers
        )
        return req.json()
    except Exception as e:
        print(f"GraphQL request error: {e}")
        return None
