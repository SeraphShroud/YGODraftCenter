#
# A simple python game server
# Alexandre Mulatinho @ 2019
#

from setuptools import setup, find_packages

setup(
    name='pyGameServer',
    version='0.0.1',
    description='A simple python generic game server',
    author='Alexandre Mulatinho',
    author_email='alex@mulatinho.net',
    url='https://github.com/mulatinho/pyGameServer',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
