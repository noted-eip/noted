import requests


def request(endpoint, query, headers=None):
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
