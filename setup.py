from setuptools import setup, find_packages

setup(
    name="time_tracker",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests", "datetime", "json", "dateutil", "decouple", "pandas",
        "base64", "numpy", "logging", "re", "os", "sys", "dotenv"
    ],
)
