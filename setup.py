from setuptools import setup, find_packages


# Read tehe requirements
def read_requirements():
    with open("requirements.txt", "r") as f:
        return f.read().splitlines()

setup(
    name="mein_package",
    version="0.1.0",
    packages=find_packages(),
    install_requires=read_requirements(),
    python_requires=">=3.7",
    description="This package is the connection to the 'HUBII Rec.' application.",
    author="Elias Müller",
    author_email="elias.mueller@kit.edu",
    url="https://github.com/dein_repo/mein_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)