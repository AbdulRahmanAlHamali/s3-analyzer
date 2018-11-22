from setuptools import setup

setup(name='s3_analyzer',
      version='0.1',
      description='Usage analyzer for AWS S3',
      url='https://github.com/AbdulRahmanAlHamali/s3_analyzer',
      author='AbdulRahman AlHamali',
      author_email='a.alhamali93@gmail.com',
      license='MIT',
      packages=['s3_analyzer'],
      entry_points = {
          'console_scripts': ['s3_analyzer=s3_analyzer.__main__:main']
      },
      install_requires=[
        'altgraph==0.16.1',
        'boto3==1.9.48',
        'botocore==1.12.48',
        'docutils==0.14',
        'future==0.17.1',
        'jmespath==0.9.3',
        'macholib==1.11',
        'pefile==2018.8.8',
        'python-dateutil==2.7.5',
        's3transfer==0.1.13',
        'six==1.11.0',
        'tabulate==0.8.2',
        'urllib3==1.24.1'
      ],
      zip_safe=False)