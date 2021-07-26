import setuptools

setuptools.setup(
    install_requires=["requests", "pandas", "numpy"],
    name="h2no",
    version="0.0.1",
    author="Eran Duchan",
    author_email="nope@none.com",
    description="Creates OpenSprinkler water usage summaries",
    url="https://github.com/pavius/h2no",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
