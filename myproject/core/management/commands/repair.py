import subprocess

from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Combo command to format, lint and verify codebase'

    def add_arguments(self, parser):
        parser.add_argument(
            '-ch', '--changes', action='store_true', help='Apply command on changed files only'
        )

    def handle(self, *args, **kwargs):

        # check if command will run on local changes only
        changes_only = kwargs['changes']
        changed_files = None

        if changes_only:
            git_diff_process = subprocess.run(
                ["git", "diff-index", "--name-only", "--diff-filter=d", "HEAD"], stdout=subprocess.PIPE
            )
            grep_process = subprocess.run(
                ["grep", "-E", ".py$"], input=git_diff_process.stdout, stdout=subprocess.PIPE
            )
            sed_process = subprocess.run(
                ["sed", "s/^myproject/./"], input=grep_process.stdout, capture_output=True
            )

            if sed_process.stdout:
                changed_files = sed_process.stdout.decode("utf8").strip().split("\n")
            else:
                print('Cannot find local changes ... abort batman --changes')
                return

        # parse commands
        files_to_affect = changed_files if changed_files else "."
        commands = [
            ["pip", "check"],
            ["black", "-S", "--config", "../pyproject.toml", *files_to_affect],
            ["flake8", *files_to_affect] if changed_files else ["flake8", "."],
            ["docformatter", "-r", "-e", "env", "venv", "-i", *files_to_affect],
            # TODO: add mypy static type checking ... on implementing check conflicts in style with black & flake8
            # TODO: add isort for imports sorting ... on implementing check conflicts in style with black & flake8
        ]

        # excute commands
        for command in commands:
            subprocess.run(command, check=False)
