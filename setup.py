from setuptools import setup

setup(name='assemblyStats',
      version='1.1.0',
      description='A script to evaluate the assembly of a given genome.',
      author='Wenchao Lin',
      author_email='linwenchao@yeah.net',
      url='https://github.com/WenchaoLin/assemblyStats',
      packages=['.'],
      keywords=['bioinformatics', 'genome statics', 'scaffold N50'],
      entry_points={
        'console_scripts': [
            'assemblyStats = assemblyStats:main'
        ]
      }
)