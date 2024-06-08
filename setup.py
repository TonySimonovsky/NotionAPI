from setuptools import setup, find_packages

setup(
    name="notionapi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pydantic",
        "typing"
    ],
    author="Tony AI Champ",
    author_email="tony@aicha.mp",
    description="A Python module for interacting with the Notion API",
    url="https://github.com/TonySimonovsky/NotionAPI",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)