from datetime import datetime

from django.conf import settings

from git import InvalidGitRepositoryError, Repo

from {app_name} import __version__

from ..utils import get_environment_color


def git_env_settings(request):
    try:
        repo = Repo(search_parent_directories=True)
    except InvalidGitRepositoryError:
        return {
            "ENVIRONMENT_BUILD": settings.BUILD_INFO,
            "ENVIRONMENT_COLOR": settings.ENVIRONMENT_COLOR,
            "ENVIRONMENT_VERSION": __version__,
        }

    # Get Git version tag
    tag = next((tag for tag in repo.tags if tag.commit == repo.head.commit), None)
    if tag:
        tagged_version = tag.name
        branch_name = "main"
    else:
        tagged_version = "Undefined"
        branch_name = str(repo.active_branch)

    build_date = datetime.fromtimestamp(repo.head.commit.committed_date).strftime("%d.%m.%Y %H:%M")
    build_info = f"{tagged_version} - {branch_name} - {repo.head.commit.hexsha} - {build_date}"

    return {
        "ENVIRONMENT_BUILD": build_info,
        "ENVIRONMENT_COLOR": get_environment_color(branch_name),
        "ENVIRONMENT_VERSION": __version__,
    }
