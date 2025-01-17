from setuptools import setup, find_packages

setup(
    name="pvgispy",
    version="0.1.3",
    description="An inofficial interface for the PVGIS API by the EU Science Hub",
    url="https://github.com/jannikobenhoff/pvgispy",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests"
    ],
    license='MIT',
)
