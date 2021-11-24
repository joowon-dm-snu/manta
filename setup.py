from setuptools import setup, find_packages

with open("requirements.txt") as file:
    requirements = file.read().splitlines()

setup(
    name="manta-client",
    version="0.1.0",
    description="A CLI and library for interacting with the Manta Engine.", 
    author="coxwave",
    author_email="support@manta.coxwave.com",
    url="https://github.com/coxwave/manta",
    download_url="https://github.com/coxwave/manta",
    license="MIT license",
    packages=find_packages(), # TODO: (kjw) need change to packages & packages_dir
    include_package_data=True,
    zip_safe=False,
    keywords=["deep learning", "logging", "tracking", "automation", "AI"], 
    python_requires=">=3.6",
    setup_requires=[],
    install_requires=requirements,
    extras_require={},
    project_urls={
        "Bug Tracker": "https://github.com/coxwave/manta/issues",
        "Documentation": "",  # TODO: (kjw) need change
        "Source Code": "https://github.com/coxwave/manta",
    },
    entry_points={
        "console_scripts": [
            "manta=manta_client.cli.entry:cli",  # TODO: (kjw) need change
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",

        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
        
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

        # Specify the Python versions you support here.  # TODO: (kjw) need change
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    test_suite="tests",
    tests_require="", # TODO: (kjw) need change
)