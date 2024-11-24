from setuptools import find_packages, setup

with open("./requirements.txt", "r") as f:
    requirements = [l.strip() for l in f.readlines() if len(l.strip()) > 0]

setup(
    name="multiview-datasets-dev",
    version="1.0.24.11.24",
    packages=find_packages(),
    install_requires=requirements,
    package_data={
        "multiview_datasets": ["config/**"],
    },
    author="Enrique Solarte",
    author_email="enrique.solarte.pardo@gmail.com",
    description=("A collection of datasets for multiview"),
    license="BSD",
)
