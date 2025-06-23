"""
Setup file for the IMDB Movie Graph package.
"""

from setuptools import setup, find_packages

setup(
    name="imdb_graph",
    version="0.1.0",
    description="Interactive graph visualization of movie relationships based on IMDB data",
    author="Kalon",
    packages=find_packages(),
    install_requires=[
        "requests",
        "matplotlib",
        "python-dotenv",
        "pyvis",
    ],
    entry_points={
        'console_scripts': [
            'imdb-graph-build=imdb_graph.main:main',
            'imdb-graph-visualize=imdb_graph.main:visualize_graph',
        ],
    },
    include_package_data=True,
    package_data={
        'imdb_graph': [
            'static/css/*.css',
            'static/js/*.js',
            'static/*.html',
            'templates/*.html',
        ],
    },
)
