from setuptools import setup, find_packages

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name='mobify',
    version='0.1.0',
    author='Maciej Brencz',
    author_email='maciej.brencz@gmail.com',
    description='Download a webpage as an e-book',
    url='https://github.com/macbre/mobify',
    keywords='epub mobi ebook html converter',
    packages=find_packages(),
    install_requires=[
        'docopt==0.6.2',
        'ebooklib==0.17.1',
        'lxml==4.6.3',
        'requests==2.26.0',
    ],
    extras_require={
        'dev': [
            'coverage==5.5',
            'pylint==2.10.2',
            'pytest==6.2.5',
            'pytest-cov==2.12.1'
        ]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mobify=mobify.cli:main',
        ],
    },
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)
