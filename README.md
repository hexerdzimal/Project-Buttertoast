
# Project-Buttertoast

**Buttertoast** is an innovative application designed to hide TrueCrypt containers inside various file formats. Using a unique polyglot technique, it embeds the container in such a way that it remains both encrypted and functional as a TrueCrypt volume, while also appearing to be a different file type, such as a WAV file or PNG image. This method has successfully bypassed detection tools like `tchunt` and other common verification methods.

With a user-friendly interface and support for a variety of file formats, **Buttertoast** offers a flexible and secure way to store sensitive data invisibly. It also supports plugin extensibility, so anyone with basic Python knowledge can add support for new file formats.

## Features

- **TrueCrypt Container Hiding**: Seamlessly embed TrueCrypt containers inside various file formats (e.g., WAV, PNG, ICO, SVG, BMP).
- **Polyglot Technology**: The TrueCrypt container is hidden within the file without disrupting its functionality, making it appear as a normal file type (like a WAV or PNG) while still being usable as a TrueCrypt volume.
- **Multiple File Formats Supported**: Includes built-in plugins for several file types such as ICO, SVG, WAV, TIFF, PNG, HTML, and more.
- **User Interface**: Both a graphical user interface (GUI) and a terminal user interface (TUI) are available.
- **Plugin Extensibility**: The application allows for easy addition of new plugins to support additional file formats. Anyone with basic Python knowledge can develop custom plugins.
- **Cross-Platform**: Supports all major operating systems that can run Python interpreters.

## Installation

### Step 1: Clone the Repository

First, clone the repository to your local machine:
```bash
git clone https://github.com/hexerdzimal/project-buttertoast.git
```

### Step 2a: Install Dependencies

Install the required dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Step 3a: Run the Application

To start the application, run the following command:

  ```bash
  python __main__.py
  ```

## OR

### Step 2b: Install the whole package
Alternatively you can use the pip installer

```bash
pip install .
```
### Step 3b: Run the Application

To start the application, run the following command:

  ```bash
  buttertoast
  ```
in this mode you can either start the UI or use its CLI with 
```bash
buttertoast -cli <HostPath> <TCVolumePath> <password> <PolyglotNameAndPath>
```

  The first time you run the application, it will start in the terminal user interface (TUI). You can set preferences in the settings to launch with the desired UI (GUI or TUI) in the future.

## Usage

### Hiding a TrueCrypt Container (GUI)

1. **Select the Host**: Choose the file in which you want to hide the TrueCrypt container (e.g., a WAV or PNG file).
2. **Select the TrueCrypt Volume**: Choose the TrueCrypt Volume, that you want to hide
3. **Select the output filename and path**: Choose the path and filename of the polyglot file that will be generated
4. **Provide the Password**: Enter the password that was used to create the TrueCrypt volume. This is necessary because the header of the container needs to be modified. If you consider this "sus", check the cryptomator files, to understand the procedure.
5. **Start the Process**: Click "Execute" to embed the container into the selected file. The file will remain usable as the original format while secretly containing the encrypted container. The file can also be mounted in TrueCrypt.


### Hiding a TrueCrypt Container (TUI)

1. **Select option 1 in the main menu**: to navigate to the main funcionality.
2. **Select the host file** Choose the host file that sould contain the tc-volume after buttertoasting it.
3. **Select the TrueCrypt Volume**: Choose the TrueCrypt Volume, that you want to hide
4. **Provide the Password**: Enter the password that was used to create the TrueCrypt volume. This is necessary because the header of the container needs to be modified. If you consider this "sus", check the cryptomator files, to understand the procedure.
5. **Choose polyglot filename and path**: Choose a name and folder to save the polyglot file.
6. **Check input** You can now check the input and change something by entering the according number, or: 
7. **Start the Process**: Select "Start data processing" to embed the container into the selected file. The file will remain usable as the original format while secretly containing the encrypted container. The file can also be mounted in TrueCrypt. 

### Hiding a TrueCrypt Container (CLI)

use
```bash
buttertoast -cli <HostPath> <TCVolumePath> <password> <PolyglotNameAndPath>
```
You also can activate a verbose mode by adding -v if you want to:
```bash
buttertoast -cli -v <HostPath> <TCVolumePath> <password> <PolyglotNameAndPath>
```

**Note**: No data is stored, corrupted, or shared. The password is only used to modify the container header and is not saved.


### Plugin System

The application supports plugins to extend its functionality. You can add new plugins for additional file types by placing them in the `plugins` directory. 

- **Plugin Development**: While creating plugins requires basic Python knowledge, it also requires an understanding of how to hide data within the bytecode of files. This is not a trivial task and requires a deeper understanding of file structures and byte-level manipulation.

## Preferences

You can change these preferences:
- **usage of the gui**: if false, you will use the textbased user interface
- **verbose-mode**: if true you will get additional info what the tool is actually doing
- **auto-check**: if true (please pay attention to the info below) the generated polyglot file will be checked by `tchungnt` automatically. You will get the vital information about the outcome.

## tchuntng-autocheck

This tool uses the `subprocess` library to start and use other processes. If you have installed and added `tchungnt` to your system and PATH, buttertoast is able to use `tchungnt` to check if your generated file is considered "encrypted" by `tchungnt`. 

## Security

- **Polyglot Technology**: The container is hidden in such a way that it behaves like a normal file, bypassing common detection tools and methods (e.g., `tchunt`).
- **Encryption**: The TrueCrypt container remains fully encrypted and secure.
- **Cross-Platform Support**: The application works on all operating systems that support Python 3.x, such as Windows, macOS, and Linux.

## Technical Details

- **Programming Language**: Python 3.13
- **Dependencies**: The necessary libraries are listed in `requirements.txt`. Key libraries include:
   - `cryptography` for secure encryption
   - `Pillow` for image handling
   - `PySide6` for the gui
   - `importlib` to make the plugins work
   - and more.
- **Supported Operating Systems**: Any OS that can run Python 3.x (Windows, macOS, Linux)

### Key Dependencies:
```
backports.tarfile==1.2.0
cryptography==43.0.3
docopt==0.6.2
fpdf==1.7.2
importlib-metadata==8.0.0
jaraco.collections==5.1.0
jinja2==3.1.4
pillow==11.0.0
platformdirs==4.2.2
pyinstaller==6.11.1
pyside6==6.8.0.2
pytest==8.3.4
rich==13.9.4
tomli==2.0.1
yarg==0.1.10

```

## Limitations

- **File Formats**: TrueCrypt volumes can only be hidden in file formats for which a functioning plugin exists. Please check the available file types in the program itself by using "List plugins" or refer to the "plugins" folder.
- **Container Size**: Containers can be any size, but "unusually large files" (relative to their file type) may raise suspicion. For example, HTML files are typically much smaller than WAV files, so large HTML files will stand out more than large WAV files.
- **Plugin Creation**: While the plugin system is designed to be easily extensible, creating plugins requires basic Python knowledge and a deeper understanding of bytecode manipulation and how to hide data within files.
- **True Crypt Encryption Mode**: For now only supports AES encrypted files (SHA-512)

## Future Plans

- **Multi-Language Support**: Plans to add support for multiple languages to make the application more accessible.
- **Additional Encryption Algorithms**: Future updates may include support for other encryption algorithms.
- **Further Features**: Ongoing development may add additional features, such as webbased user interfaces or other cryptographic techniques.

## Contributing

This project was developed by **Fabian Kozlowski, Stefan Leippe, Malte Muthesius, and Matthias Ferstl** as part of a university (Fernuniversitaet Hagen) project. Contributions and improvements are welcome!

## License

This project is licensed under the GNU General Public License (GPL) v3. See the `LICENSE` file for more details.
