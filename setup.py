import setuptools


setuptools.setup(
    name='sydjango',
    version='0.0.1',
    packages=setuptools.find_packages(),
    install_requires=[
        'Django',
        'django-post-office',
        'django-object-actions',
        'django-import-export',
        'django-admin-rangefilter',
        'django-disposable-email-checker',
    ],
    extras_require={
        'test': [
            'coverage',
            'django-dynamic-fixture',
            'pytest-cov',
            'pytest-django',
            'tox',
            'mock',
            'coverage',
            'django-webtest',
        ],
        'dev': [
            'django-debug-toolbar',
        ]
    },
)
