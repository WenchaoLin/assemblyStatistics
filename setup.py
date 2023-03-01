from setuptools import setup

file_path = 'README.md'

setup(name='assemblyStatistics',
      version='1.1.1',
      description='A script to evaluate the assembly of a given genome.',
      long_description=open(file_path, encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      license='GPL-3',
      author='Wenchao Lin',
      include_package_data=True,
      author_email='linwenchao@yeah.net',
      url='https://github.com/WenchaoLin/assemblyStatistics',
      packages=['.'],
      keywords=['bioinformatics', 'genome statics', 'scaffold N50'],
      entry_points={
        'console_scripts': [
            'assemblyStatistics = assemblyStatistics:main'
        ]
      }
)