"""Setup file for easy installation."""

from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="loganom",
    version="0.0.7",
    author="Danilo G. Baio",
    author_email="dbaio@bsd.com.br",
    description="Log analyzer to discover anomalies",
    license='BSD2CLAUSE',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/dbaio/loganom",
    project_urls={
        "Documentation": "https://loganom.readthedocs.io/en/latest/",
    },
    platforms=["any"],
    packages=['loganom'],
    package_dir={"loganom": "loganom"},
    include_package_data=True,
    entry_points={"console_scripts": ["loganom = loganom.main:main"]},
    install_requires=[
        'dnspython',
        'requests',
        'marrow.mailer'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False,
)
