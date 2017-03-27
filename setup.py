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
          'boto3==1.4.0',
          'pymssql==2.1.3',
          'dnspython==1.15.0',
          'sleekxmpp==1.3.1',
          'awscli'
      ]
)
