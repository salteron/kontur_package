from subprocess import run

from kontur.package import log


def execute(command, raise_on_failure=True):
    log(f'$ {command}')

    completed_process = run(command, shell=True, check=False, capture_output=True)
    result = Result(completed_process)

    if raise_on_failure and not result.is_successful():
        raise Error(result.stderr())

    return result


class Result:
    def __init__(self, completed_process):
        self._completed_process = completed_process

    def is_successful(self):
        return not self._completed_process.returncode

    def stdout(self):
        return self._completed_process.stdout.strip().decode()

    def stderr(self):
        return self._completed_process.stderr.strip().decode()


class Error(Exception):
    pass
