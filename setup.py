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
        'ebooklib==0.19',
        'lxml==6.0.0',
        'requests==2.32.4',
    ],
    extras_require={
        'dev': [
            'coverage==7.9.2',
            'pylint==3.3.7',
            'pytest==8.4.1',
            'pytest-cov==6.2.1'
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ]
)
