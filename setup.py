from setuptools import find_packages, setup

setup(
    name='logging_gli',
    packages=find_packages(include=['logging_gli']),
    version='0.1.0',
    description='My first Python library',
    author='Resa Renaldy',
    license='GLI',
    setup_requires=['google-cloud-logging==2.6.0']
)

