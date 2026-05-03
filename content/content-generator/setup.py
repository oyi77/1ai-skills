from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("SKILL.md", "r", encoding="utf-8") as fh:
    skill_description = fh.read()

setup(
    name="content-generator-skill",
    version="1.0.0",
    author="Paijo",
    author_email="paijo@example.com",
    description="Multi-provider automated video content generation platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oyi77/1ai-skills/tree/master/content/content-generator",
    packages=find_packages(where="scripts"),
    package_dir={"": "scripts"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.11",
    install_requires=[
        # Core dependencies - using built-in urllib, no external HTTP libs
    ],
    entry_points={
        "console_scripts": [
            "content-generator=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["../config.yaml", "../README.md", "../SKILL.md"],
        "references": ["../references/*.md"],
        "templates": ["../templates/*"],
    },
)
