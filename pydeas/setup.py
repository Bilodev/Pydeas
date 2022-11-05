from setuptools import setup, find_packages
import os
import codecs


VERSION = '1.0.2'
DESCRIPTION = 'A simple db package'

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    LONG_DESCRIPTION = "\n" + fh.read()

# Setting up
setup(
    name="pydeas",
    version=VERSION,
    author="Bilodev (Antonio Bilotta)",
    author_email="bilotta.antonio.biz@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",                       
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['rich', 'pandas'],
    keywords=['python', 'database', 'csv',
              'relational database', 'relational', 'pydesDb', 'pydes'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
