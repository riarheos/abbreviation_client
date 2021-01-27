from setuptools import setup

setup(
    name='abbreviation_client',
    version='1.0',
    packages=['abbreviation_client'],
    url='https://github.com/riarheos/abbreviation_client',
    license='GPL',
    author='Pavel Pushkarev',
    author_email='riarheos@gmail.com',
    description='The abbreviation client command line library',
    install_requires=[
        'termcolor',
    ],
)
