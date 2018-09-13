from unittest.mock import Mock, patch

from kontur.package.models import Package


@patch('kontur.package.models.execute')
def test_current(execute):
    def side_effect(command, *_args, **_kwargs):
        if command == 'python setup.py --name':
            mock = Mock()
            mock.stdout.return_value = 'name'
            return mock
        elif command == 'python setup.py --version':
            mock = Mock()
            mock.stdout.return_value = 'version'
            return mock

    execute.side_effect = side_effect

    package = Package.current()

    assert package.name == 'name'
    assert package.version == 'version'


def test_str():
    package = Package(name='name', version='version')
    assert str(package) == 'name==version'


@patch('kontur.package.models.rmtree')
@patch('kontur.package.models.execute')
def test_build(execute, rmtree):
    package = Package(name='name', version='version')
    package.build()

    rmtree.assert_called_with('dist')
    execute.assert_called_with('python setup.py sdist --dist-dir dist bdist_wheel --dist-dir dist')
