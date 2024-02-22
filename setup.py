from setuptools import find_packages, setup

setup(
    name='tiktoksellerapi',
    packages=find_packages(include=['tiktoksellerapi']),
    version='0.1.0',
    description='My first Python library',
    author='Me',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)