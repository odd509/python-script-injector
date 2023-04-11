# python-script-injector
A python script that can encrypt and inject itself into other Python scripts in the same directory.

This Python script is designed to infect other Python files in the current directory with a copy of itself, but encrypted with a custom encryption function.

##Usage
To use this script, simply run it in the same directory as the Python files you wish to infect. The script will automatically detect all Python files in the directory (excluding itself), inject a copy of its encrypted code into them, and then replace the original files with the infected copies.

##Custom Encryption and Decryption Functions
The script uses two custom functions encrypt() and decrypt() to encrypt and decrypt the code that is injected into other Python files. These functions use a custom XOR-based encryption algorithm and a Base64 encoding scheme to obfuscate the injected code.

##Delimiters
The script uses two delimiters to mark the beginning and end of the original code and the encrypted code.

# DELIMITER:START marks the beginning of the original code.
# DELIMITER:END marks the end of the original code and the beginning of the encrypted code.
# DELIMITER:CRYPTO marks the end of the custom encryption and decryption functions.
Additional Information
The script requires Python 3.x to run.
The script only infects Python files with the extension .py.
The script uses a checksum of each file's name as a unique identifier to avoid infecting the same file multiple times.
The injected code is saved to a new file with the extension .injected before being replaced with the original file.
The script does not modify or delete any files other than the ones it infects.
This script is for educational purposes only and should not be used to harm or damage any systems or files.
License
This script is licensed under the MIT License.
