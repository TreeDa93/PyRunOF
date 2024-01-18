from setuptools import setup, find_packages
import pyRunOF

setup(name='pyRunOF',

      version=pyRunOF.__version__,

      url='https://github.com/TreeDa93/PyRunOF/tree/main',

      license='MIT',

      author='Smolyanov Ivan',

      author_email='i.a.smolyanov@gmail.com',

      description='Test project!!!',

      packages=find_packages(),
      include_package_data=True,
      
      install_requires=['numpy', 'matplotlib'],

      long_description=open('README.md').read(),
      zip_safe=False
      )
