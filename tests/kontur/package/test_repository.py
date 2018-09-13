from unittest.mock import Mock, patch

from kontur.package.models import Repository


@patch('kontur.package.models.execute')
def test_str(execute):
    repository = Repository('remote')

    result = Mock()
    result.stdout.return_value = 'http://example.com'
    execute.return_value = result

    assert str(repository) == 'http://example.com'
    execute.assert_called_with('git remote get-url remote')


@patch('kontur.package.models.execute')
def test_tag(execute):
    repository = Repository('remote')
    repository.tag('1.0.0')

    execute.assert_called_with('git tag -a -m "Version 1.0.0" v1.0.0')


@patch('kontur.package.models.execute')
def test_push_tags(execute):
    repository = Repository('remote')
    repository.push_tags()

    execute.assert_called_with('git push --tags remote')
