#!/bin/bash

setup_git() {
  git config --global user.email "travis@travis-ci.com"
  git config --global user.name "Travis CI"
}

commit_pg_releases_file() {
  git add -f pgdoc_datatype_parser/pg-releases.json
  git add -f pgdoc_datatype_parser/__init__.py
  git add -f setup.cfg
  git commit -m "Update pg-releases.json file ($TRAVIS_BUILD_NUMBER)"
}

push() {
  git remote set-url origin \
    "https://mondeja:$GITHUB_PASSWORD@github.com/mondeja/pgdoc-datatype-parser.git" \
    > /dev/null 2>&1
  git push --quiet origin HEAD:master
}

setup_git
commit_pg_releases_file
push
