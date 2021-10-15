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
    install_requires=["pydantic[dotenv]", "httpx", "authlib", "tenacity"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==6.2.2"],
    test_suite="tests",
)
