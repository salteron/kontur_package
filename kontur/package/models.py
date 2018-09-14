from shutil import rmtree

from kontur.package.commands import execute


class Package:
    BUILD_DIR = 'dist'
    BUILD_CMD = 'python setup.py sdist --dist-dir {directory} bdist_wheel --dist-dir {directory}'
    CURRENT_NAME_CMD = 'python setup.py --name'
    CURRENT_VERSION_CMD = 'python setup.py --version'

    @classmethod
    def current(cls):
        name = execute(cls.CURRENT_NAME_CMD).stdout()
        version = execute(cls.CURRENT_VERSION_CMD).stdout()

        return cls(name=name, version=version)

    def __init__(self, name, version, build_dir=BUILD_DIR):
        self.name = name
        self.version = version
        self.build_dir = build_dir

    def __str__(self):
        return f'{self.name}=={self.version}'

    def build(self):
        rmtree(self.build_dir, ignore_errors=True)
        cmd = self.BUILD_CMD.format(directory=self.build_dir)
        return execute(cmd)


class PYPI:
    CONTAINS_CMD = 'pip download --no-deps --dest /tmp --index-url {pypi.url} {package.name}=={package.version}'
    UPLOAD_CMD = 'twine upload --repository-url {pypi.url} ' \
                 '--username {pypi.user_name} --password {pypi.user_password} {directory}/*'

    def __init__(self, url, user_name, user_password):
        self.url = url
        self.user_name = user_name
        self.user_password = user_password

    def __str__(self):
        return self.url

    def contains(self, package):
        cmd = self.CONTAINS_CMD.format(pypi=self, package=package)
        return execute(cmd, raise_on_failure=False).is_successful()

    def upload_from(self, directory):
        cmd = self.UPLOAD_CMD.format(pypi=self, directory=directory)
        return execute(cmd)


class Repository:
    ADD_TAG_CMD = 'git tag -a -m "Version {version}" {tag_name}'
    PUSH_TAGS_CMD = 'git push --tags {url_or_remote}'

    def __init__(self, url_or_remote):
        self.url_or_remote = url_or_remote

    def __str__(self):
        return self.url_or_remote

    def tag(self, version):
        tag_name = f'v{version}'
        cmd = self.ADD_TAG_CMD.format(version=version, tag_name=tag_name)
        return execute(cmd)

    def push_tags(self):
        cmd = self.PUSH_TAGS_CMD.format(url_or_remote=self.url_or_remote)
        return execute(cmd)
