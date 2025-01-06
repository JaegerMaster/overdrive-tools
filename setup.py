from setuptools import setup, find_packages
import os

# Read the README file if it exists, otherwise use a basic description
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "Tools for downloading and processing OverDrive audiobooks"

setup(
    name="overdrive-tools",
    version="3.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Tools for downloading and processing OverDrive audiobooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/overdrive-tools",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "rich>=10.0.0",
        "mutagen>=1.45.0",
    ],
    extras_require={
        'beets': ['beets>=1.6.0'],
    },
    entry_points={
        "console_scripts": [
            "overdrive-tools=overdrive_tools.cli:main",
        ],
    },
)
