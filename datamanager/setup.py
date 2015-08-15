import versioneer
from ez_setup import use_setuptools

try:
    from setuptools import setup
except ImportError:
    use_setuptools()
    #from distutils.core import setup
    from setuptools import setup

config = {
    'install_requires': ['pandas', 'logbook'],
    'packages': ['datamanager'],
    'entry_points' : {
        'console_scripts' : ['datamanager = datamanager.main:runtasks']
    },
    'name': 'datamanager'
}

setup(version=versioneer.get_version(),
  cmdclass=versioneer.get_cmdclass(), **config)
