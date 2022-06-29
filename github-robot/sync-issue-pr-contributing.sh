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
)

set -e

mkdir -p ./tmp

for repo in ${REPOSITORIES[@]}; do
    git clone "git@github.com:noted-eip/$repo" ./tmp/$repo
    mkdir -p ./tmp/$repo/.github
    mkdir -p ./tmp/$repo/.github/ISSUE_TEMPLATE
    cp ./.github/ISSUE_TEMPLATE/*.md ./tmp/$repo/.github/ISSUE_TEMPLATE
    cp ./.github/PULL_REQUEST_TEMPLATE.md ./tmp/$repo/.github
    cp ./CONTRIBUTING.md ./tmp/$repo/CONTRIBUTING.md
    git -C ./tmp/$repo add -A
    git -C ./tmp/$repo commit -sm "feat: sync pr, issue template and contributing"
    git -C ./tmp/$repo push
done

rm -r ./tmp
