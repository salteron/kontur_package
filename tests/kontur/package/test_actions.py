from unittest.mock import Mock, patch

from kontur.package.actions import push_tags, release, released, tag, upload
from kontur.package.models import PYPI, Package, Repository


@patch('kontur.package.models.execute')
def test_released_when_package_is_already_released(execute):
    pypi = PYPI('url', 'user-name', 'user-password')
    package = Package(name='name', version='version')

    result = Mock()
    result.is_successful.return_value = True
    execute.return_value = result

    assert released(package, pypi)


@patch('kontur.package.models.execute')
def test_released_when_package_is_not_released_yet(execute):
    pypi = PYPI('url', 'user-name', 'user-password')
    package = Package(name='name', version='version')

    result = Mock()
    result.is_successful.return_value = False
    execute.return_value = result

    assert not released(package, pypi)


@patch('kontur.package.models.rmtree')
@patch('kontur.package.models.execute')
def test_build(execute, rmtree):
    package = Package(name='name', version='version')
    package.build()

    rmtree.assert_called_with('dist')
    execute.assert_called_with('python setup.py sdist --dist-dir dist bdist_wheel --dist-dir dist')


@patch('kontur.package.models.execute')
def test_upload(execute):
    pypi = PYPI('url', 'user-name', 'user-password')
    package = Package(name='name', version='version')

    upload(package, pypi)

    execute.assert_called_with('twine upload --repository-url url --username user-name --password user-password dist/*')


@patch('kontur.package.models.execute')
def test_tag(execute):
    repository = Repository('remote')
    tag(repository, '1.0.0')

    execute.assert_called_with('git tag -a -m "Version 1.0.0" v1.0.0')


@patch('kontur.package.models.execute')
def test_push_tags(execute):
    repository = Repository('remote')

    def side_effect(command):
        if command == 'git remote get-url remote':
            result = Mock()
            result.stdout.return_value = 'https://example.com'
            return result

    execute.side_effect = side_effect

    push_tags(repository)

    execute.assert_called_with('git push --tags remote')


@patch('kontur.package.models.execute')
@patch('kontur.package.models.rmtree')
def test_release(_rmtree, execute):
    pypi = PYPI('url', 'user-name', 'user-password')
    package = Package(name='name', version='1.0.0')
    repository = Repository('remote')

    def side_effect(command, *_args, **_kwargs):
        if command == 'pip download --no-deps --dest /tmp --index-url url name==1.0.0':
            result = Mock()
            result.is_successful.return_value = False
            return result
        elif command == 'git remote get-url remote':
            result = Mock()
            result.stdout.return_value = 'https://example.com'
            return result

    execute.side_effect = side_effect

    release(package, pypi, repository)

    execute.assert_any_call('pip download --no-deps --dest /tmp --index-url url name==1.0.0', raise_on_failure=False)
    execute.assert_any_call('python setup.py sdist --dist-dir dist bdist_wheel --dist-dir dist')
    execute.assert_any_call('twine upload --repository-url url --username user-name --password user-password dist/*')
    execute.assert_any_call('git tag -a -m "Version 1.0.0" v1.0.0')
    execute.assert_any_call('git push --tags remote')


@patch('kontur.package.models.execute')
@patch('kontur.package.actions.push_tags')
@patch('kontur.package.actions.tag')
@patch('kontur.package.actions.upload')
@patch('kontur.package.actions.build')
def test_release_when_already_released(build, upload, tag, push_tags, execute):
    pypi = PYPI('url', 'user-name', 'user-password')
    package = Package(name='name', version='1.0.0')
    repository = Repository('remote')

    def side_effect(command, *_args, **_kwargs):
        if command == 'pip download --no-deps --dest /tmp --index-url url name==1.0.0':
            result = Mock()
            result.is_successful.return_value = True
            return result

    execute.side_effect = side_effect

    release(package, pypi, repository)

    build.assert_not_called()
    upload.assert_not_called()
    tag.assert_not_called()
    push_tags.assert_not_called()
