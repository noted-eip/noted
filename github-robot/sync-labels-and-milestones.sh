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
    "infra"
    "mobile"
)

for repo in ${REPOSITORIES[@]}; do
    echo "Creating labels for '$ORG/$repo'"
    gh api --method POST -H "Accept: application/vnd.github.v3+json" "/repos/$ORG/$repo/labels" -f name='noted/story' -f description='This issue will be included in the PLD' -f color='58259F' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" "/repos/$ORG/$repo/labels" -f name='noted/backlog' -f description='Story for a later sprint' -f color='58259F' --silent
    gh api --method POST -H "Accept: application/vnd.github.v3+json" "/repos/$ORG/$repo/labels" -f name='noted/archive' -f description='Story from an old sprint' -f color='58259F' --silent
done
