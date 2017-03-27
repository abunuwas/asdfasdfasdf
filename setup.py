from setuptools import setup, find_packages

setup(name='controller',
      version='1.0',
      description='Device Test Contrller API',
      author='Jose Haro',
      author_email='jharoperalta@intamac.com',
      url='',
      license='',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=[
          'curl==2017.0.1',
          'docker==2.1.0',
          'Flask==0.12',
          'Flask-HTTPAuth==3.2.2',
          'Flask-RESTful==0.3.5'
      ]
)
