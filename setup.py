from setuptools import setup, find_packages


setup(
    name='bookrunner',
    version='0.2',
    license='MIT',
    author="Celest",
    author_email='hello@celest.moe',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/CeIest/BW-preview-DLer',
    install_requires=[
          'requests',
          'urllib3',
          'click',
      ],

)
