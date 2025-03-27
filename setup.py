from setuptools import setup, find_packages

setup(
    name="webp-converter",
    version="1.0.0",
    py_modules=["main"],
    packages=find_packages(),
    install_requires=[
        "pillow==11.1.0",
    ],
    entry_points={
        "console_scripts": [
            "webp-converter=main:main",
        ],
    },
    author="farithadnan",
    description="A CLI tool to convert images to WebP format.",
    url="https://github.com/farithadnan/webp-converter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)