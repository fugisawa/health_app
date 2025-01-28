"""Setup configuration for the health protocol dashboard."""
from setuptools import setup, find_packages

setup(
    name="health-protocol",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "streamlit>=1.22.0",
        "plotly>=5.15.0",
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "watchdog>=3.0.0",
        "jinja2>=3.0.0",
        "pytest>=7.0.0",
    ],
    extras_require={
        "dev": [
            "black",
            "isort",
            "mypy",
            "pytest-cov",
        ]
    },
    entry_points={
        "console_scripts": [
            "health-protocol=app.main:main",
        ],
    },
    author="Daniel Fugisawa",
    description="A comprehensive health protocol tracking dashboard",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="health, protocol, tracking, dashboard",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 