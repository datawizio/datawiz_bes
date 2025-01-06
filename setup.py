from setuptools import find_packages, setup

from bes import __version__

setup(
    name="bes",
    packages=find_packages(exclude=["tests"]),
    version=__version__,
    description="BES Package of Datawiz.io",
    author="Datawiz.io",
    author_email="support@datawiz.io",
    license="MIT",
    install_requires=["pydantic==2.8.2", "httpx==0.27.0", "authlib==1.2.0", "tenacity==8.2.2", "python-dotenv==1.0.0"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest>=6.2.5"],
    test_suite="tests",
)
