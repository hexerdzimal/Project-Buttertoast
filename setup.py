# Buttertoast Copyright (C) 2024 Matthias Ferstl, Fabian Kozlowski, Stefan Leippe, Malte Muthesius
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# For more information, contact: mail@matthias-ferstl.de


from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    rlong_description = fh.read()


setup(
    # Basic information
    name="Buttertoast",  # toolname
    version="0.9.0",       # Version, using SemVer 
    author="Matthias Ferstl, Fabian Kozlowski Stefan Leippe, Malte Muthesius", 
    author_email="mail@matthias-ferstl.de",  # E-Mail-Adress
    description="A tool to hide TrueCrypt container in polyglot-files",  # shortdescription
    long_description=rlong_description,  # long description, opens README-File
    long_description_content_type="text/markdown",  # readme Content type
    url="https://github.com/hexerdzimal/Project-Buttertoast", 

    # Packages and requirements

    packages=find_packages(),  # look for packege data
    include_package_data=True,  # also incule package data
    install_requires = [
        "backports.tarfile==1.2.0",
        "cryptography==43.0.3",
        "docopt==0.6.2",
        "fpdf==1.7.2",
        "importlib-metadata==8.0.0",
        "jaraco.collections==5.1.0",
        "jinja2==3.1.4",
        "pillow==11.0.0",
        "platformdirs==4.2.2",
        "pyinstaller==6.11.1",
        "pyside6==6.8.0.2",
        "pytest==8.3.4",
        "tomli==2.0.1",
        "yarg==0.1.10",
    ],

    python_requires=">=3.11",  # minimum Python version


    # entrypoint
    entry_points={
    "console_scripts": [
        "buttertoast=buttertoast:main",  
    ],
},

    # classifiers 
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: GNU V. 3 License", 
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta"
    ],

    # metadata
    license="GNU V. 3",  # Type of license
    project_urls={  # additional info
        "Bug Tracker": "https://github.com/hexerdzimal/Project-Buttertoast/issues",
        "Source Code": "https://github.com/hexerdzimal/Project-Buttertoast",
        "License": "https://www.gnu.org/licenses/gpl-3.0.html"
    },
)