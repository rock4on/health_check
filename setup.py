"""Setup configuration for DCMA Health Check package."""
from setuptools import setup, find_packages

setup(
    name="dcma-healthcheck",
    version="0.1.0",
    description="DCMA 11-point schedule quality analysis tool",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "openai>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "dcma-check=dcma_healthcheck.main:main",
        ]
    },
)