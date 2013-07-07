from setuptools import setup

setup(
    name='dicm',
    get_version_from_scm=True,
    description='Dependency Injection Concisely Managed',
    setup_requires=[
        'hgdistver',
    ],
    packages=[
        'dicm',
    ]
)
