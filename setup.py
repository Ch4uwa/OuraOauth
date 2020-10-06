from setuptools import find_packages, setup


with open("README.md", "r") as rm:
    long_description = rm.read()

with open("requirements.txt", "r") as f:
    requirements = f.read()


setup(
    name="ouraOauth",
    version="0.0.1",
    author="Martin Karlsson",
    author_email="mrtn.karlsson@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    python_requires=">=3.8",
)
