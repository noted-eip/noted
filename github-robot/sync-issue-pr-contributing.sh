# Repositories in which to sync issues and pr templates, contributing
# guidelines and licensing.
REPOSITORIES=(
    "protorepo"
    "compose"
    "api-gateway"
    "accounts-service"
    "notes-service"
    "recommendations-service"
    "web-desktop"
    "mobile"
)

mkdir -p ./tmp

for repo in ${REPOSITORIES[@]}; do
    git clone "git@github.com:noted-eip/$repo" ./tmp/$repo
    mkdir -p ./tmp/$repo/.github
    mkdir -p ./tmp/$repo/.github/ISSUE_TEMPLATE
    mkdir -p ./tmp/$repo/docs
    mkdir -p ./tmp/$repo/docs/assets
    cp ./.github/ISSUE_TEMPLATE/*.md ./tmp/$repo/.github/ISSUE_TEMPLATE
    cp ./.github/PULL_REQUEST_TEMPLATE.md ./tmp/$repo/.github
    cp ./docs/assets/*.png ./tmp/$repo/docs/assets
    cp ./docs/CONTRIBUTING.md ./tmp/$repo/docs
    cp ./LICENSE ./tmp/$repo/LICENSE
    git -C ./tmp/$repo add -A
    git -C ./tmp/$repo commit -sm "feat: sync pr, issue template and contributing"
    git -C ./tmp/$repo push
done

rm -rf ./tmp
