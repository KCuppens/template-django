#!/usr/bin/env python3
import subprocess

import environ
from git import Repo


env = environ.Env()
env.read_env(".env")


def print_title(title):
    print()
    print(80 * "-")
    print(title.center(80))
    print(80 * "-")


def stop_service():
    print_title("Stop webapp with supervisor")
    subprocess.run("supervisorctl stop {app_name}", shell=True)
    print_title("Stop celery with supervisor")
    subprocess.run("supervisorctl stop celery", shell=True)


def start_service():
    print_title("Start webapp with supervisor")
    subprocess.run("supervisorctl start {app_name}", shell=True)
    print_title("Start celery with supervisor")
    subprocess.run("supervisorctl start celery", shell=True)


def get_current_tag_name():
    repo = Repo(search_parent_directories=True)
    tag = next((tag for tag in repo.tags if tag.commit == repo.head.commit), None)
    if tag:
        tagged_version = tag.name
    else:
        tagged_version = repo.head.commit.hexsha
    return tagged_version


def update_sources():
    print_title("Update sources")
    repo = Repo(search_parent_directories=True)
    repo.git.fetch()
    print("Available versions:")
    all_tags = [tag.name for tag in repo.tags]
    print("\n".join(all_tags))
    last_tag = all_tags[-1]

    tag_number = None
    while tag_number not in all_tags:
        tag_number = input(f"Enter tag number to update to [{last_tag}]: ")
        if tag_number == "":
            tag_number = last_tag
        if tag_number not in all_tags:
            print("Invalid tag number")
        if tag_number == "skip":
            break
        if tag_number == "dev":
            repo.git.checkout("dev")
            repo.git.pull()
            break
    if tag_number not in ["skip", "dev"]:
        repo.git.checkout(tag_number)

    return tag_number


def install_requirements():
    print_title("Install production requirements")
    subprocess.run("../venv/bin/pip install -r requirements/production.txt", shell=True)


def migrate_db():
    print_title("Do database migrations")
    subprocess.run(
        "../venv/bin/python manage.py migrate --settings={app_name}.settings.production",
        shell=True,
    )


def collect_static():
    print_title("Collect static files")
    subprocess.run(
        "../venv/bin/python manage.py collectstatic "
        "--noinput --settings={app_name}.settings.production",
        shell=True,
    )


if __name__ == "__main__":
    previous_version = get_current_tag_name()
    stop_service()
    new_version = update_sources()
    install_requirements()
    migrate_db()
    collect_static()
    start_service()
    print_title("Successfully updated from {} to {}".format(previous_version, new_version))
