from setuptools import setup

from skillful import __version__
from skillful import __doc__ as description


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

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
                'skillful.tests',],
      install_requires=['six',],
      test_suite='nose.collector',
      tests_require=['nose'])
