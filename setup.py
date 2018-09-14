from setuptools import find_namespace_packages, setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

tests_dependencies = ['pytest', 'pytest-cov']

setup(
    name='kontur_package',
    version='1.0.4',
    description='TODO: description',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=['twine', 'click'],
    setup_requires=['pytest-runner'],
    tests_require=tests_dependencies,
    extras_require={
        'test': tests_dependencies
    },
    url='https://git.skbkontur.ru/custom_dev/kontur_package',
    packages=find_namespace_packages(include=['kontur.*']),
    namespace_packages=['kontur'],
    entry_points={
        'console_scripts': [
            'kontur-package=kontur.package.cli:cli'
        ]
    },
    maintainer='kontur custom',
    maintainer_email='custom@skbkontur.ru',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent'
    ]
)
