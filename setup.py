from pathlib import Path

from setuptools import find_namespace_packages, setup

HERE = Path(__file__).parent
LONG_DESCRIPTION = HERE.joinpath("README.md").read_text(encoding="utf-8")

setup(
    name="devterminal",
    version="1.0.0",
    author="Minkx1",
    description="Lightweight desktop terminal app with custom command handling and a Tkinter-based UI.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="",
    package_dir={"": "."},
    packages=find_namespace_packages(include=["libs.*"]),
    py_modules=["terminal"],
    install_requires=["customtkinter"],
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Framework :: Tkinter",
        "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
)
