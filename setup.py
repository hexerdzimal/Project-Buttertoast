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



setup(
    # Basic information
    name="Buttertoast",  # toolname
    version="0.9.0",       # Version, using SemVer 
    author="Matthias Ferstl, Fabian Kozlowski Stefan Leippe, Malte Muthesius", 
    author_email="mail@matthias-ferstl.de",  # E-Mail-Adress
    description="A tool to hide TrueCrypt container in polyglot-files",  # shortdescription
    long_description=open("README.md").read(),  # long description, opens README-File
    long_description_content_type="text/markdown",  # readme Content type
    url="https://github.com/hexerdzimal/Project-Buttertoast", 

    # Packages and requirements

    packages=find_packages(),  # look for packege data
    include_package_data=True,  # also incule package data
    install_requires = [
        "altgraph==0.17.4",
        "certifi==2024.8.30",
        "cffi==1.17.1",
        "charset-normalizer==3.4.0",
        "click==8.1.7",
        "colorama==0.4.6",
        "cryptography==43.0.3",
        "fpdf==1.7.2",
        "idna==3.10",
        "iniconfig==2.0.0",
        "Jinja2==3.1.4",
        "MarkupSafe==3.0.2",
        "packaging==24.2",
        "pefile==2023.2.7",
        "pillow==11.0.0",
        "pluggy==1.5.0",
        "pycparser==2.22",
        "pyinstaller==6.11.1",
        "pyinstaller-hooks-contrib==2024.10",
        "PySide6==6.8.0.2",
        "PySide6_Addons==6.8.0.2",
        "PySide6_Essentials==6.8.0.2",
        "pytest==8.3.4",
        "pywin32-ctypes==0.2.3",
        "requests==2.32.3",
        "setuptools==75.6.0",
        "shiboken6==6.8.0.2",
        "urllib3==2.2.3"
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