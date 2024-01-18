from setuptools import setup, find_packages

setup(name='pyRunOF',

      version='0.1b',

      url='https://github.com/TreeDa93/PyRunOF/tree/main',

      license='MIT',

      author='Smolyanov Ivan',

      author_email='i.a.smolyanov@gmail.com',

      description='Test project!!!',

      packages=find_packages(exclude=['tests', 'solvers']),

      long_description=open('README.md').read(),

      zip_safe=False)
