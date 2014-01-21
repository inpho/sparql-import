from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
NEWS = open(os.path.join(here, 'NEWS.md')).read()


version = '0.1'

install_requires = [
    # List your project dependencies here.
    # http://pythonhosted.org/setuptools/setuptools.html#declaring-dependencies 
    "rdflib>=3.2.0,<=3.2.99",
    "rdfextras>=0.4"
]


setup(name='sparql-import',
    version=version,
    description="This is a script to merge data from LODE into InPhO",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Database',
        'Topic :: Utilities'
        # List at: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='sparql linkeddata lod',
    author='InPhO Project',
    author_email='inpho@indiana.edu',
    url='https://github.com/inpho/sparql-import',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires
)
