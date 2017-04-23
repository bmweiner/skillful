import sys
import os
from setuptools import setup

__version__ = '0.7.1'
__description__ = 'A Python package for building Alexa skills.'

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

try:
    import pypandoc
    dirname = os.path.dirname(__file__)
    txt = pypandoc.convert(os.path.join(dirname, 'README.md'), 'rst')
    with open(os.path.join(dirname, 'README.rst'), 'w') as f:
        f.write(txt)
except(IOError, ImportError):
    pass

setup(name='skillful',
      version=__version__,
      author='bmweiner',
      author_email='bmweiner@users.noreply.github.com',
      url='https://github.com/bmweiner/skillful',
      description=__description__,
      classifiers = [
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          ],
      platforms=['py27', 'py35'],
      license='MIT License',
      packages=['skillful',
                'skillful.tests'],
      install_requires=['six'],
      setup_requires=[] + pytest_runner,
      tests_require=['pytest'])
