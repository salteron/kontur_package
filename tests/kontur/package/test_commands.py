from subprocess import CompletedProcess
from unittest.mock import Mock, patch

from kontur.package.commands import Result, execute


def test_result_is_successful():
    successfully_completed_process = Mock(spec=CompletedProcess)
    successfully_completed_process.returncode = 0
    assert Result(successfully_completed_process).is_successful()

    failed_completed_process = Mock(spec=CompletedProcess)
    failed_completed_process.returncode = 1
    assert not Result(failed_completed_process).is_successful()


def test_result_stdout():
    completed_process = Mock(spec=CompletedProcess)
    completed_process.stdout = b' hello '
    assert Result(completed_process).stdout() == 'hello'


@patch('kontur.package.commands.run')
def test_execute(run):
    completed_process = Mock(spec=CompletedProcess)
    completed_process.stdout = b' hello '
    completed_process.returncode = 0
    run.return_value = completed_process

    execute('echo')
    run.assert_called_with('echo', shell=True, check=True, capture_output=True)

    execute('echo', raise_on_failure=False)
    run.assert_called_with('echo', shell=True, check=False, capture_output=True)

    result = execute('echo')
    assert result.stdout() == 'hello'
    assert result.is_successful()


@patch('kontur.package.commands.run')
@patch('kontur.package.commands.log')
def test_execute_logging(log, _run):
    execute('echo')
    log.assert_called_with('$ echo')
