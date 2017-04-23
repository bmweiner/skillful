import sys
from setuptools import setup

from skillful import __version__
from skillful import __doc__ as description

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    try:
        with open('README.md') as file:
            long_description = file.read()
    except(IOError):
        long_description = 'See github repository.'

setup(name='skillful',
      version=__version__,
      author='bmweiner',
      author_email='bmweiner@users.noreply.github.com',
      url='https://github.com/bmweiner/skillful',
      description=description,
      long_description=long_description,
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
