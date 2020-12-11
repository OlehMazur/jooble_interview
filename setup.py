import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jooble-jobtest-pkg-oleg-mazur",
    version="0.0.1",
    author="Oleg Mazur",
    author_email="olegmazurbidev@gmail.com",
    description="A test interview package ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OlehMazur/jooble_interview",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)