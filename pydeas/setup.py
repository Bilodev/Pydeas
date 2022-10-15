from setuptools import setup, find_packages


VERSION = '0.1.7'
DESCRIPTION = 'A simple db package'
LONG_DESCRIPTION = 'A package that allows to build simple databases, in an easy and fast way.'

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
    keywords=['python', 'database', 'csv', 'relational database', 'relational', 'pydeDb', 'pyde'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)