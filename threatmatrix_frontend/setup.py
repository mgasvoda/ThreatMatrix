import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="threatmatrix_frontend",
    version="0.0.1",
    author="Michael Gasvoda",
    description="Conflict data visualization and analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mgasvoda/ThreatMatrix",
    packages=setuptools.find_packages(),
    install_requires=[
        'sqlalchemy>=1.2.7',
        'pandas>=0.23.0',
        'folium>=0.6.0',
        'bokeh>=1.0.0',
        'flask>=1.0.2',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)