from setuptools import setup

setup(
     name='item_catalog',
     packages=['item_catalog'],
     include_package_data=True,
     install_requires=[
        'flask',
        'SQLAlchemy',
        'oauth2client',
        'requests'
     ],
)
