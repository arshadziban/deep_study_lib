# setup.py
"""
Case Study Package Setup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="deep-study",
    version="1.0.4",
    author="Shah Md. Arshad Rahman Ziban",
    author_email="arshadziban031201@gmail.com",
    description="Deep Study - Dataset Overview and Feature Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arshadziban/deep_study_lib",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "deep_study": ["templates/*.html"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.4.0",
        "jinja2>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
        ],
    },
    keywords=[
        "data-analysis",
        "correlation",
        "feature-importance",
        "machine-learning",
        "pandas",
        "profiling",
        "eda",
        "exploratory-data-analysis",
    ],
)