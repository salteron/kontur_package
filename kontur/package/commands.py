from subprocess import run

from kontur.package import log


def execute(command, dry=False, raise_on_failure=True):
    prefix = '(dry) ' if dry else ''
    log(f'>> {prefix}{command}')

    if dry:
        command = f'echo {command}'

    completed_process = run([command], shell=True, check=raise_on_failure, capture_output=True)

    if raise_on_failure:
        completed_process.check_returncode()

    return Result(completed_process)


class Result:
    def __init__(self, completed_process):
        self._completed_process = completed_process

    def is_successful(self):
        return not self._completed_process.returncode

    def stdout(self):
        return self._completed_process.stdout.strip().decode()
