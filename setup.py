import setuptools
import re

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as rf:
    requirements = rf.read().splitlines()

def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop), open(project + '/__init__.py').read())
    return result.group(1)

setuptools.setup(
    name="anatools",
    version=get_property('__version__', 'anatools'),
    author="Rendered AI, Inc",
    author_email="support@rendered.ai",
    description="Tools for development with the Rendered.ai Platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://rendered.ai",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    scripts=[
        "anatools/bin/ana", 
        "anatools/bin/anadeploy", 
        "anatools/bin/anamount",
        "anatools/bin/anautils"],
    package_data={"": ["*.yml"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"],
    python_requires='>=3.6',
)
