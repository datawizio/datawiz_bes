from setuptools import find_packages, setup

from datawiz_bes import __version__

setup(
    name="datawiz_bes",
    packages=find_packages(exclude=["tests"]),
    version=__version__,
    description="BES Package of Datawiz.io",
    author="Datawiz.io",
    author_email="support@datawiz.io",
    license="MIT",
    install_requires=["pydantic"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==6.2.2"],
    test_suite="tests",
)
