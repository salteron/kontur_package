import click

from kontur.package import actions
from kontur.package.models import PYPI, Package, Repository

# TODO: remote PYPI constants
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


pypi_url_option = click.option('--pypi-url', default=PYPI_URL, callback=validate_presence)
pypi_user_name_option = click.option('--pypi-user-name', default=PYPI_USER_NAME, callback=validate_presence)
pypi_user_password_option = click.option('--pypi-user-password', default=PYPI_USER_PASSWORD, callback=validate_presence)
repository_remote_option = click.option('--repository-remote',
                                        default=DEFAULT_REPOSITORY_REMOTE, callback=validate_presence)


@cli.command()
@pypi_url_option
@pypi_user_name_option
@pypi_user_password_option
@repository_remote_option
def release(pypi_url, pypi_user_name, pypi_user_password, repository_remote):
    """Releases current version of package unless already released"""

    pypi = PYPI(url=pypi_url, user_name=pypi_user_name, user_password=pypi_user_password)
    repository = Repository(remote=repository_remote)

    actions.release(package=Package.current(), pypi=pypi, repository=repository)


@cli.command()
@pypi_url_option
@pypi_user_name_option
@pypi_user_password_option
def released(pypi_url, pypi_user_name, pypi_user_password):
    """Checks whether current version of package have been already released"""

    pypi = PYPI(url=pypi_url, user_name=pypi_user_name, user_password=pypi_user_password)

    actions.released(package=Package.current(), pypi=pypi)


@cli.command()
def build():
    """Builds package distributions (default dir: dist)"""

    actions.build(package=Package.current())


@cli.command()
@pypi_url_option
@pypi_user_name_option
@pypi_user_password_option
def upload(pypi_url, pypi_user_name, pypi_user_password):
    """Uploads package distributions from dist/ to package index"""

    pypi = PYPI(url=pypi_url, user_name=pypi_user_name, user_password=pypi_user_password)

    actions.upload(package=Package.current(), pypi=pypi)


@cli.command()
@repository_remote_option
def tag(repository_remote):
    """Tags HEAD with current version number"""

    repository = Repository(remote=repository_remote)

    actions.tag(repository=repository, version=Package.current().version)


@cli.command()
@repository_remote_option
def push_tags(repository_remote):
    """Pushes tags to remote repository"""

    repository = Repository(remote=repository_remote)

    actions.push_tags(repository=repository)


if __name__ == '__main__':
    cli()
