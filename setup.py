"""
Verification Frameworks from AI Research Village

Battle-tested verification tools and frameworks developed through 
AI agent collaboration in the AI Village project.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="verification-frameworks",
    version="1.0.0",
    author="AI Village Agents",
    author_email="village@theaidigest.org",
    description="Verification tools developed through AI agent collaboration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ai-village-agents/village/verification-frameworks",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: System :: Archiving",
        "Topic :: Validation",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies are minimal - frameworks designed to be lightweight
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "examples": [
            "requests>=2.28.0",
            "pandas>=1.5.0",
            "numpy>=1.24.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "verify-wave=verification_frameworks.wave.cli:main",
            "verify-archival=verification_frameworks.archival.cli:main",
            "verify-cold=verification_frameworks.protocol.cli:main",
        ],
    },
    include_package_data=True,
    project_urls={
        "Source": "https://gitlab.com/ai-village-agents/village/verification-frameworks",
        "Documentation": "https://gitlab.com/ai-village-agents/village/verification-frameworks/-/blob/main/docs/",
        "AI Village": "https://theaidigest.org/village",
    },
)
