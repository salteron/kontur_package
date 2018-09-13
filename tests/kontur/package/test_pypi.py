from unittest.mock import Mock, patch

from kontur.package.models import PYPI, Package


def test_str():
    pypi = PYPI('url', 'user-name', 'user-password')
    assert str(pypi) == 'url'


@patch('kontur.package.models.execute')
def test_contains_when_package_is_already_released(execute):
    pypi = PYPI('url', 'user-name', 'user-password')
    package = Package(name='name', version='version')

    result = Mock()
    result.is_successful.return_value = True
    execute.return_value = result

    assert pypi.contains(package)
    execute.assert_called_with('pip download --no-deps --dest /tmp --index-url url name==version',
                               raise_on_failure=False)


@patch('kontur.package.models.execute')
def test_contains_when_package_is_not_released_yet(execute):
    pypi = PYPI('url', 'user-name', 'user-password')
    package = Package(name='name', version='version')

    result = Mock()
    result.is_successful.return_value = False
    execute.return_value = result

    assert not pypi.contains(package)
    execute.assert_called_with('pip download --no-deps --dest /tmp --index-url url name==version',
                               raise_on_failure=False)


@patch('kontur.package.models.execute')
def test_upload_from(execute):
    pypi = PYPI('url', 'user-name', 'user-password')
    directory = 'dist'

    pypi.upload_from(directory)

    execute.assert_called_with('twine upload --repository-url url --username user-name --password user-password dist/*')
