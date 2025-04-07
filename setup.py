from setuptools import setup, find_packages

setup(
    name="graph_feature",
    version="0.1",
    packages=find_packages(),
    install_requires=["numpy"],
    author="Frederik Mortensen Dam",
    author_email="Fdam39@gmail.com",
    description="GVC feature extraction package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DenatYeti/graph_feature",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
