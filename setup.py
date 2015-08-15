import versioneer
from setuptools import setup

config = {
    'install_requires': ['pandas', 'logbook'],
    'packages': ['datamanager'],
    'entry_points' : {
        'console_scripts' : ['datamanager = datamanager.main:runtasks']
    },
    'version': versioneer.get_version(),
    'cmdclass': versioneer.get_cmdclass()
}

setup(**config)
