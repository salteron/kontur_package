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

# TODO: для организации cli попробовать click

args:
    - pypi_url, pypi_user_name, pypi_password
    - repository url / remote
'''

pypi_url = 'http://localhost:8080'
pypi_user_name = 'user'
pypi_user_password = 'user'
pypi = PYPI(url=pypi_url, user_name=pypi_user_name, user_password=pypi_user_password)

repository_url = 'upstream'
repository = Repository(remote=repository_url)

package = Package.current()


def release():
    actions.release(package=package, pypi=pypi, repository=repository)


def released():
    return actions.released(package=package, pypi=pypi)
