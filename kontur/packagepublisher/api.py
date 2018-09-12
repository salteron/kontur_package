# TODO: переименовать проект в releaser

from subprocess import run


class ExecutionResult:
    def __init__(self, completed_process):
        self._completed_process = completed_process

    def is_successful(self):
        return not self._completed_process.returncode

    def stdout(self):
        return self._completed_process.stdout.strip().decode()


def execute(command, dry=False, raise_on_failure=True):
    prefix = '(dry) ' if dry else ''
    print(f'>> {prefix}{command}')

    if dry:
        command = f'echo {command}'

    completed_process = run([command], shell=True, check=raise_on_failure, capture_output=True)

    if raise_on_failure:
        completed_process.check_returncode()

    return ExecutionResult(completed_process)


class Package:
    @staticmethod
    def name():
        return execute('python setup.py --name').stdout()

    @staticmethod
    def version():
        return execute('python setup.py --version').stdout()


class PYPI:
    # $PYPI_URL
    # $PYPI_USERNAME
    # $PYPI_PASSWORD
    def __init__(self, url, user_name, user_password):
        self.url = url
        self.user_name = user_name
        self.user_password = user_password

    def contains(self, name, version):
        is_version_published_cmd = (
            f'pip download --no-deps --dest /tmp --index-url {self.url} '
            f'{name}=={version}'
        )

        return execute(is_version_published_cmd, raise_on_failure=False).is_successful()


class Uploader:
    def __init__(self, pypi):
        self._pypi = pypi

    def upload_from(self, directory):
        cmd = f'twine upload --repository-url {self._pypi.url} --username {self._pypi.user_name} --password {self._pypi.user_password} {directory}/*'
        return execute(cmd, dry=True)


class Builder:
    def build(self, directory):
        return execute(f'python setup.py sdist --dist-dir {directory} bdist_wheel --dist-dir {directory}', dry=True)


class Git:
    def __init__(self, remote_url):
        self._remote_url = remote_url

    def tag(self, version):
        tag_name = f'v{version}'
        execute(f'git tag -a -m "Version {version}" {tag_name}', dry=True)
        execute(f'git push --tags {self._remote_url}', dry=True)


def publish():
    '''
    Сценарий
    
    Разработчик меняет версию пакета, мерджит реквест в мастер.
    
    На мердж в мастер настроен запуск скрипта, который проверяет, выпущена ли версия, и, если нет, выпускает,
    и ставит и пушит таг.
    '''

    '''
        Возможно необходимо организовать несколько команд для этой утилиты:
            - publish
            - check (которая проверит, что все условия соблюдены: проставлены необходимые переменные окружения,
                     можно достать версию и имя пакета)
    
    
    # узнать имя пакета в текущей директории которого находимся
    python setup.py --name
    
    # узнать версию пакет в в текущей директории которого находимся
    # python setup.py --version
    
    # git в ci не установлен 
    
    # необходимо ставить таг на текущую ветку
    
    # поскольку утилита не дает возможность менять версию, то и коммитить `bump version` не нужно
    
    # TODO: сделать одним классам много методов
    # TODO: сделать метод проверки аргументов
    # TODO: переименовать в gitlab в группе PYPI_USERNAME (и подобное) в KONTUR_PYPI_USERNAME, а в секции билда
    # присвоить переменной PIP_USERNAME=KONTUR_PYPI_USERNAME
    
    # TODO: команды вынести в константы
    
    # TODO: для организации cli попробовать click
    
    args:
        - pypi_url, pypi_user_name, pypi_password
        - repository url / remote
    '''

    name = Package.name()
    version = Package.version()

    pypi = PYPI(url='https://pypi.testkontur.ru', user_name='$PYPI_USERNAME', user_password='$PYPI_PASSWORD')
    is_published = pypi.contains(name=name, version=version)

    if is_published:
        print(f'{name}=={version} is published. Nothing to do')
    else:
        print(f'{name}=={version} is not yet published')

        Builder().build(directory='dist')
        Uploader(pypi).upload_from(directory='dist')
        remote = 'upstream'
        Git(remote).tag(version)
