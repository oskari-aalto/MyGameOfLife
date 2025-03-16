import os.path

from setuptools import setup


def readme_file_contents():
    readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.rst')
    with open(readme_path) as readme_file:
        file_contents = readme_file.read()
    return file_contents


setup(
    name='mygameoflife',
    version='1.0.0',
    description='Conway\'s Game of Life implemented with PyGame.',
    long_description=readme_file_contents(),
    url='https://github.com/mrWawe/MyGameOfLife',
    author='mrWawe',
    author_email='email@email.com',
    license='GPL-3.0',
    packages=['mygameoflife'],
    scripts=[
        'bin/mygameoflife',
        'bin/mygameoflife.bat',
    ],
    zip_safe=False,
    install_requires=[
        'pygame'
    ]
)
