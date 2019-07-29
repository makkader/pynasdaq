from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='pynasdaq',
      version='0.2.1',
      description='Retrieve NASDAQ stock and dividend data',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/makkader/pynasdaq',
      author='Mak Kader',
      author_email='abdul.kader880@gmail.com',
      license='MIT',
      packages=['pynasdaq'],
      install_requires=[
          'pandas',
          'lxml',
          'requests'
      ],
      zip_safe=False)
