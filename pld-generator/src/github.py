# TODO: whole github graphql shit
# https://stackoverflow.com/questions/70600049/github-projects-beta-how-to-get-the-data-from-a-view-in-the-api
# https://docs.github.com/en/graphql/reference/objects#projectv2
# Best graphql request for project for now (too much info, to shorten) :
"""
    {
  node(id: "My_Project_ID") {
    ... on ProjectNext {
      items(first: 100, after: null) {
        edges {
          cursor
        }
        nodes {
          content {
            ... on Issue {
              title
              body
              assignees(first: 1) {
                nodes {
                  login
                }
              } 
              milestone {
                title
              }
              labels(first: 5) {
                nodes {
                  name
                }
              }
              repository{
                name
              }
            }
          }
          fieldValues(first: 15) {
            nodes {
              value
              projectField {
                name
                settings
              }
            }
          }
        }
      }
    }
  }
}
"""
