import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imdb-cli",
    version="0.1.0",
    author="Bardi Harborow",
    author_email="bardi@bardiharborow.com",
    description="A command-line tool for retrieving an artist's filmography from IMDb.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bardiharborow/imdb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'imdb = imdb.__main__:main'
        ]
    },
)
