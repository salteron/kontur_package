from kontur.package import log


def release(package, pypi, repository):
    if released(package, pypi):
        return

    build(package)
    upload(package, pypi)
    tag(repository, package.version)
    push_tags(repository)


def released(package, pypi):
    is_released = pypi.contains(package)

    if is_released:
        log(f'Package {package} has been already released')
    else:
        log(f'Package {package} has not been released yet')

    return is_released


def build(package):
    log(f'Building package {package}')
    return package.build()


def upload(package, pypi):
    log(f'Uploading package {package} to {pypi}')
    return pypi.upload_from(package.build_dir)


def tag(repository, version):
    log(f'Setting tag for version {version}')
    return repository.tag(version)


def push_tags(repository):
    log(f'Pushing tags to {repository}')
    return repository.push_tags()
