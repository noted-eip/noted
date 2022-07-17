#!/bin/bash

# Github organization. 
ORG="noted-eip"

# Repositories in which to create issues and milestones.
REPOSITORIES=(
    "protorepo"
    "compose"
    "api-gateway"
    "accounts-service"
    "notes-service"
    "recommendations-service"
    "web-desktop"
    "noted"
    "mobile"
)

for repo in ${REPOSITORIES[@]}; do
    echo "Creating labels for '$ORG/$repo'"
    gh api --method POST -H "Accept: application/vnd.github.v3+json" "/repos/$ORG/$repo/labels" -f name='noted/story' -f description='This issue will be included in the PLD' -f color='58259F' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" "/repos/$ORG/$repo/labels" -f name='noted/backlog' -f description='Story for a later sprint' -f color='58259F' --silent

    echo "Creating milestones for '$repo'"
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Early July 2022' -f state='open' -f description='' -f due_on='2022-07-16T00:00:00Z' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Late July 2022' -f state='open' -f description='' -f due_on='2022-08-01T00:00:00Z' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Early August 2022' -f state='open' -f description='' -f due_on='2022-08-16T00:00:00Z' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Late August 2022' -f state='open' -f description='' -f due_on='2022-09-01T00:00:00Z' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Early September 2022' -f state='open' -f description='' -f due_on='2022-09-16T00:00:00Z' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Late September 2022' -f state='open' -f description='' -f due_on='2022-10-01T00:00:00Z' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Early October 2022' -f state='open' -f description='' -f due_on='2022-10-16T00:00:00Z' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Late October 2022' -f state='open' -f description='' -f due_on='2022-11-01T00:00:00Z' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Early November 2022' -f state='open' -f description='' -f due_on='2022-11-16T00:00:00Z' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Late November 2022' -f state='open' -f description='' -f due_on='2022-12-01T00:00:00Z' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Early December 2022' -f state='open' -f description='' -f due_on='2022-12-16T00:00:00Z' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" /repos/$ORG/$repo/milestones -f title='Late December 2022' -f state='open' -f description='' -f due_on='2023-01-01T00:00:00Z' --silent
done
