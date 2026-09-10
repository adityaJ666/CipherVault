def scramble(text, key):
    result = ""

    for i, char in enumerate(text):
        shift = ord(key[i % len(key)])
        new_char = chr((ord(char) + shift) % 256)
        result += new_char

    return result


def unscramble(text, key):
    result = ""

    for i, char in enumerate(text):
        shift = ord(key[i % len(key)])
        new_char = chr((ord(char) - shift) % 256)
        result += new_char

    return result


print("===== KEY SCRAMBLER =====")

text = input("Enter text: ")
key = input("Enter secret key: ")

if len(key) == 0:
    print("Error: Secret key cannot be empty.")
else:
    scrambled = scramble(text, key)

    print("\nScrambled text:")
    print(scrambled)

    original = unscramble(scrambled, key)

    print("\nDecrypted text:")
    print(original)