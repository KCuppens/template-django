# Branching and merging stategy

[TOC]


We implement git flow, please see [full doc](https://hackmd.io/42FtzZzBQhKDLJ1XgKsl0g?both). Here you'll find in details how it should work.


## Feature branches

:::warning

We are using a rebase strategy for feature branches.

**Do not touch feature branches that don’t belong to you** without consent of their developers - since rebasing requires force pushing, your changes could be easily lost. Feature branches are there for development, and are therefore subject to having their history changed and overridden.

:::
1. Create issue in Jira, copy the git branch creation from there (it will get issue number in name)
2. Find a good prefix (e.g. `feat`, `imp`, `fix`)
```
git checkout dev
git pull
git checkout -b imp/RXSG-1244-homogeneize-the-ubiquitous-language
```
3. While developing try to rebase on a daily basis, to avoid painful conflict resolution
```
git checkout dev
git pull
git checkout imp/RXSG-1244-homogeneize-the-ubiquitous-language
git rebase dev
# deal with (hopefully) small merge conflicts
git push --force
```
4. While developing commit and push your modification every day. Use as comment beginning with WIP (Work In Progress) if code is not really ready yet.
5. Add a line to the changelog for the issue you are solving
6. Run a last rebase from `dev` just before making your pull request. Ensure there is no database migration issue (see [below](#Migrations)):
```
python manage.py makemigrations --dry-run --check
```
After the pull request has been properly reviewed, the integrator will "squash and merge" your branch, so that the history is not full of WIP and other funny comments. Use the jira task title as first line of commit, and potentially part of its content to the message.


## Hotfixes
1. Create branch
```
git checkout master
git pull
git checkout -b hotfix/RXSG-1244-vat-rates
```
2. fix the issue
3. add a test for the fix
4. update version number (in `{app_name}/__init__.py`)
5. update the `CHANGELOG`, add new release
6. Make the pull request (check that it os a PR to main rather tha develop)
7. Make sure someone else reviews the code, never trust yourself on production hotfixes, you are blinded by the urgent character of the issue.
8. Merge
9. Tag
10. Get it back to develop, be sure there will be some conflicts to solve :(.
```
git checkout dev
git pull
git merge main
git push
```

## Database migrations
Database schema and data migrations are one of the most complicated problem to solve when working as a team.
### The issue
At some point, you'll encounter this message:
```
$ python manage.py migrate
CommandError: Conflicting migrations detected; multiple leaf nodes in the migration graph: (0002_longer_titles, 0002_author_nicknames).

The reason is that we got 2 migrations with the same id. Django does not understand which one to apply first.
The cause is probably 2 branches developed in parallel, touching models in the same app.

```
                  +--> 0002_author_nicknames
                 /
0001_initial +--|
                 \
                  +--> 0002_longer_titles
```

To fix this situation it is best to rename your file. E.g. rename `0002_longer_titles` into `0003_longer_titles` and
change the dependency in your migration to point to `0002_author_nicknames`. In essence you are rebasing rather than merging.

```
0001_initial --> 0002_author_nicknames --> 0003_longer_titles
```

### Other rules to follow

1. Always name your migration (i.e. don't let `0004_auto_xxx.py` be committed). The mitigation of migration will be done manually at some point, and the dev will appreciate.
2. Never create a migration that can't be run backwards. That is needed with data migrations. At some point, your migration will need to be reverted (e.g. `manage.py migrate myapp 0003`), and renamed so that another migration is inserted in between.
3. Before pull requesting, try to squeeze your multiple new migrations into a single one (that is inside every modified app).
4. Always rebase your branch on dev before pull requesting it. Check that you don't have issues with `python manage.py makemigrations --dry-run --check`

