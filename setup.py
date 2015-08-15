from setuptools import setup

config = {
    'install_requires': ['pandas', 'logbook'],
    'packages': ['datamanager'],
    'entry_points' : {
        'console_scripts' : ['datamanager = datamanager.main:enter']
    }}

setup(**config)
