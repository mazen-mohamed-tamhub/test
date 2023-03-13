from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = 'fix'

    def handle(self, *args, **kwargs):
        commands = [
            ["pip", "check"],
            ["black", "-S", "."],
            ["flake8", "--extend-exclude", "venv", "--max-line=120", "."],
        ]
        for command in commands:
            subprocess.run(command, check=False)
            # try:
            #     subprocess.run(command, check=True)
            # except subprocess.CalledProcessError as exc:
            #     print(
            #         f"Command {command} failed because the process "
            #         f"did not return a successful return code.\n{exc}"
            #     )
            # except subprocess.TimeoutExpired as exc:
            #     print(f"Command {command} timed out.\n {exc}")
