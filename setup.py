from setuptools import setup
from os import path


long_description = "Check usages in https://nbviewer.jupyter.org/github/makkader/pynasdaq/blob/master/usages.ipynb"


setup(name='pynasdaq',
      version='0.3.2',
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
