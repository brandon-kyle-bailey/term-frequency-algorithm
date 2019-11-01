from setuptools import setup

def readme():
    with open('docs/README.md') as f:
        return f.read()

setup(name='term-frequency-algorithm',
      version='0.1',
      description='representation of the term frequency algorithm.',
      long_description=readme(),
      classifiers=[
        'Programming Language :: Python :: 3.7',
        'Topic :: Term Frequency :: Algorithms',
      ],
      keywords='technical test',
      url='None',
      author='Brandon Bailey',
      author_email='brandonkylebailey@outlook.com',
      license='None',
      packages=['app'],
      # install_requires=[
      #     'Python>=3.7.3',
      # ],
      include_package_data=True,
      zip_safe=False)
