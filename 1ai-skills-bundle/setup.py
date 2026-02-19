"""
1ai-skills-bundle

A meta-package to install all 80+ 1ai-skills with a single command.
AI workforce for one-person companies.

Supports installation via:
- npm: npm install @1ai/1ai-skills-bundle
- pip: pip install 1ai-skills-bundle
"""

from setuptools import setup, find_packages
import os
import json
from pathlib import Path


# Read skill index
def get_skill_index():
    """Load the skill index data."""
    skill_index_path = Path(__file__).parent / "skill-index.json"
    if skill_index_path.exists():
        with open(skill_index_path, "r") as f:
            return json.load(f)
    return {"skills": [], "teams": []}


# Get long description from README
def get_long_description():
    """Read the README file for long description."""
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Install all 80+ 1ai-skills with a single command."


# Get requirements
def get_requirements():
    """Read requirements from requirements.txt."""
    req_path = Path(__file__).parent / "requirements.txt"
    if req_path.exists():
        with open(req_path, "r") as f:
            return [
                line.strip() for line in f if line.strip() and not line.startswith("#")
            ]
    return []


# Get skill categories for package data
skill_index = get_skill_index()
local_skills = [s for s in skill_index.get("skills", []) if s.get("source") == "local"]
external_skills = [
    s for s in skill_index.get("skills", []) if s.get("source") == "external"
]

# Package metadata
setup(
    name="1ai-skills-bundle",
    version="1.0.0",
    author="Paijo",
    author_email="paijo@example.com",
    description="Install all 80+ 1ai-skills with a single command - AI workforce for one-person companies",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/paijo/1ai-skills",
    project_urls={
        "Bug Tracker": "https://github.com/paijo/1ai-skills/issues",
        "Documentation": "https://github.com/paijo/1ai-skills#readme",
        "Source Code": "https://github.com/paijo/1ai-skills",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    platforms=["any"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    install_requires=get_requirements(),
    extras_require={
        "dev": [],
        "trading": [
            "ccxt>=2.0.0",
            "metatrader5>=5.0.0",
            "pandas>=1.5.0",
            "numpy>=1.21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "1ai-skills=list_skills:main",
        ],
    },
    package_data={
        "1ai_skills_bundle": [
            "skill-index.json",
            "README.md",
            "install.py",
        ],
    },
    include_package_data=True,
    keywords=[
        "ai",
        "skills",
        "agents",
        "automation",
        "claude",
        "opencode",
        "openclaw",
        "autonomous",
        "workflow",
        "trading",
    ],
    pythonifier_typings="py.typed",
)
