import setuptools
import tia

with open("README.md", "r") as fh:
    long_description = fh.read()

git_url = "https://github.com/eduardostarling/tia.git"

setuptools.setup(
    name=tia.__name__,
    version=tia.__version__,
    author="Eduardo Starling",
    author_email="edmstar@gmail.com",
    description="Test Impact Analysis Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=git_url,
    packages=['tia'],
    install_requires=[
        'quart',
        'sqlalchemy',
        'sqlalchemy_aio',
        'pymysql',
        'cryptography'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Source Code": git_url
    },
    python_requires='>=3.7'
)
