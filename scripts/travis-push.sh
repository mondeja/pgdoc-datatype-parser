#!/bin/bash

setup_git() {
  git config --global user.email "mondejar1994@gmail.com"
  git config --global user.name "Álvaro Mondéjar"
}

commit_pg_releases_file() {
  git checkout master
  git add pgdoc_datatype_parser/pg-releases.json
  git commit -m "Update pg-releases.json file ($TRAVIS_BUILD_NUMBER)"
}

push() {
  git remote add origin \
    https://mondeja:${GITHUB_PASSWORD}@github.com/mondeja/pgdoc-datatype-parser.git \
    > /dev/null 2>&1
  git push --quiet --set-upstream origin master
}

setup_git
commit_pg_releases_file
push
