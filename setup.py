from setuptools import setup, find_packages

from mobify.version import version

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name='mobify',
    version=version,
    author='Maciej Brencz',
    author_email='maciej.brencz@gmail.com',
    description='Download a webpage as an e-book',
    keywords='epub mobi ebook html converter',
    packages=find_packages(),
    install_requires=[
        'docopt==0.6.2',
        'ebooklib==0.15',
        'lxml==3.4.0',
        'pylint==1.4.4',
        'pytest==2.8.2',
        'requests==2.8.0',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mobify=mobify.cli:main',
        ],
    },
)
