# Changes

Add clear description of changes.

## Code review checklist

Check all checkbox before send your code in review

- [ ] ๐งช **Test your code manually**
  - Test the functionality
  - Test if changes can impact (edge effect) other features already present
- [ ] ๐ค **Reread** your changes with [Gitk](https://www.atlassian.com/git/tutorials/gitk) or other tool to see all changes line by line
- [ ] ๐งผ **Clean up** your code:
  - Keep your code easy to understand ex: (smaller functions, explicit variables and functions names, etc)
  - Respect the [Code Style Guide](https://github.com/{app_name}/{app_name}-backend/blob/1fd7800e1a7044080d11243a671f91a6d99c528e/docs/codestyle.md)
  - Use a linter (flake8, isort, etc) or [pre-commit configuration](https://github.com/{app_name}/{app_name}-backend/blob/7f309a22b3283e0ce5ea96418e659af795864864/.pre-commit-config-ci.yaml)
- [ ] ๐ **Remove unused code**: commented code, `print()` used for test or debugging
- [ ] ๐ **Update the documentation**, if needed:
  - `README.md`
  - `docs/[explain].md`
  - In `Notion` page (for documentation)
- [ ] ๐  **Unit tests**
  - Write unit tests for all new or modified code
  - Check if all the tests pass (green)
- [ ] ๐พ **Update migrations** If there are modification in the model
  - Run command line `./manage.py makemigrations`
  - Commit migration files are generated in `./[app_label]/migrations/`
- [ ] ๐ท **Update the [`CHANGELOG.md`](https://semver.org)**
  - Format your changelog title like this: `- describes changes` with suffix [ENG-{id}]
- [ ] ๐ด **Clean the git branch**: `git rebase -i origin/dev`
  - Squash unnecessary commits on your branch, to keep clean history
  - Add clear description message merge request
  - Format Your **branch** name like this: `ENG-{id}_Description_of_your_changes}` with prefix [ENG-{id}]
  - Format your **commit** title like this: `ENG-{id}:{Description of your changes}`with prefix [ENG-{id}]
- [ ] โ๏ธ **Add a clear description of your modifications to the merge request**
- [ ] ๐ **Update the status of the issue to `CODE REVIEW` in [Notion]
