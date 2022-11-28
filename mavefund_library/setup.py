import setuptools

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name="mavefund",
    version="0.0.1",
    license="GNU",
    author="ddjerqq",
    author_email="ddjerqq@gmail.com",
    url="https://github.com/ddjerqq/mavefund",
    keywords="mavefund stocks investing data science",
    description="The official API client for the MaveFund API.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=[
        "pandas",
        "requests",
        "aiohttp",
    ],
    packages=["mavefund"],
)
