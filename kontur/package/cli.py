import click

from kontur.package import actions
from kontur.package.models import PYPI, Package, Repository

'''
https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
https://packaging.python.org/guides/single-sourcing-package-version/
https://github.com/abak-press/apress-gems/blob/master/lib/apress/gems/cli.rb


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

# TODO: сделать метод проверки аргументов
# TODO: переименовать в gitlab в группе PYPI_USERNAME (и подобное) в KONTUR_PYPI_USERNAME, а в секции билда
# присвоить переменной PIP_USERNAME=KONTUR_PYPI_USERNAME

# Использовать CI_COMMIT_SHA для передачи коммита, на который надо ставить tag
# CI_REPOSITORY_URL

apt-get install git
# add user password
git init .
git remote add upstream CI_REPOSITORY_URL
git fetch upstream
git checkout CI_COMMIT_SHA

# https://about.gitlab.com/2017/11/02/automating-boring-git-operations-gitlab-ci/
'''

PYPI_URL = 'http://localhost:8080'
PYPI_USER_NAME = 'user'
PYPI_USER_PASSWORD = 'user'

DEFAULT_REPOSITORY_REMOTE = 'upstream'


def validate_presence(_ctx, _param, value):
    if not value:
        raise click.BadParameter('value is empty!')
    return value


@click.group()
def cli():
    """Package release tool"""


@cli.command()
@click.option('--pypi-url', default=PYPI_URL, callback=validate_presence)
@click.option('--pypi-user-name', default=PYPI_USER_NAME, callback=validate_presence)
@click.option('--pypi-user-password', default=PYPI_USER_PASSWORD, callback=validate_presence)
@click.option('--repository-remote', default=DEFAULT_REPOSITORY_REMOTE, callback=validate_presence)
def release(pypi_url, pypi_user_name, pypi_user_password, repository_remote):
    """Releases current version of package unless already released"""

    pypi = PYPI(url=pypi_url, user_name=pypi_user_name, user_password=pypi_user_password)
    repository = Repository(remote=repository_remote)

    actions.release(package=Package.current(), pypi=pypi, repository=repository)


@cli.command()
@click.option('--pypi-url', default=PYPI_URL, callback=validate_presence)
@click.option('--pypi-user-name', default=PYPI_USER_NAME, callback=validate_presence)
@click.option('--pypi-user-password', default=PYPI_USER_PASSWORD, callback=validate_presence)
def released(pypi_url, pypi_user_name, pypi_user_password):
    """Checks whether current version of package have been already released"""

    pypi = PYPI(url=pypi_url, user_name=pypi_user_name, user_password=pypi_user_password)

    actions.released(package=Package.current(), pypi=pypi)


@cli.command()
def build():
    """Builds package distributions (default dir: dist)"""

    actions.build(package=Package.current())


@cli.command()
@click.option('--pypi-url', default=PYPI_URL, callback=validate_presence)
@click.option('--pypi-user-name', default=PYPI_USER_NAME, callback=validate_presence)
@click.option('--pypi-user-password', default=PYPI_USER_PASSWORD, callback=validate_presence)
def upload(pypi_url, pypi_user_name, pypi_user_password):
    """Uploads package distributions from dist/ to package index"""

    pypi = PYPI(url=pypi_url, user_name=pypi_user_name, user_password=pypi_user_password)

    actions.upload(package=Package.current(), pypi=pypi)


@cli.command()
@click.option('--repository-remote', default=DEFAULT_REPOSITORY_REMOTE, callback=validate_presence)
def tag(repository_remote):
    """Tags HEAD with current version number"""

    repository = Repository(remote=repository_remote)

    actions.tag(repository=repository, version=Package.current().version)


@cli.command()
@click.option('--repository-remote', default=DEFAULT_REPOSITORY_REMOTE, callback=validate_presence)
def push_tags(repository_remote):
    """Pushes tags to remote repository"""

    repository = Repository(remote=repository_remote)

    actions.push_tags(repository=repository)


if __name__ == '__main__':
    cli()
