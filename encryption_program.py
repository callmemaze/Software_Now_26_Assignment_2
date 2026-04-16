import os


# ============================================================
# HELPER FUNCTION: SHIFT A SINGLE CHARACTER
# ============================================================
# This function shifts a character forward or backward in the alphabet.
# It preserves case (uppercase/lowercase) and wraps around using modulo.
#
# Parameters:
#   c         → character to shift
#   shift     → number of positions to shift
#   direction → "forward" or "backward"
#
# Returns:
#   shifted character
# ============================================================

def shift_char(c, shift, direction="forward"):
    base = ord('a') if c.islower() else ord('A')
    alpha_index = ord(c) - base

    if direction == "forward":
        new_index = (alpha_index + shift) % 26
    else:
        new_index = (alpha_index - shift) % 26

    return chr(base + new_index)


# ============================================================
# ENCRYPTION FUNCTION (STRING LEVEL)
# ============================================================
# Applies encryption rules to each character in the input text.
#
# Rules:
#   - a–m → forward shift by (shift1 * shift2)
#   - n–z → backward shift by (shift1 + shift2)
#   - A–M → backward shift by shift1
#   - N–Z → forward shift by (shift2 squared)
#   - other characters → unchanged
#
# Returns:
#   encrypted string
# ============================================================

def encrypt_text(text, shift1, shift2):
    result = []

    for c in text:
        if c.islower():
            if 'a' <= c <= 'm':
                shift = shift1 * shift2
                result.append(shift_char(c, shift, "forward"))
            else:  # n-z
                shift = shift1 + shift2
                result.append(shift_char(c, shift, "backward"))

        elif c.isupper():
            if 'A' <= c <= 'M':
                shift = shift1
                result.append(shift_char(c, shift, "backward"))
            else:  # N-Z
                shift = shift2 ** 2
                result.append(shift_char(c, shift, "forward"))

        else:
            result.append(c)  # unchanged

    return "".join(result)



def decrypt_text(text, shift1, shift2):
    return None #None


# ============================================================
# FILE ENCRYPTION FUNCTION
# ============================================================
# Reads raw_text.txt, encrypts it, and writes to encrypted_text.txt
# Includes error handling for file operations.
# ============================================================

def encrypt_file(input_path, output_path, shift1, shift2):
    try:
        with open(input_path, "r") as f:
            text = f.read()

        encrypted = encrypt_text(text, shift1, shift2)

        with open(output_path, "w") as f:
            f.write(encrypted)

    except Exception as e:
        print("Encryption error:", e)



def decrypt_file(input_path, output_path, shift1, shift2):
    return None



# ============================================================
# VERIFICATION FUNCTION
# ============================================================
# Compares original file with decrypted file to ensure correctness.
#
# Returns:
#   True  → if files match
#   False → otherwise
# ============================================================


def verify_files(file1, file2):
    try:
        with open(file1, "r") as f1, open(file2, "r") as f2:
            text1 = f1.read()
            text2 = f2.read()

        if text1 == text2:
            print("Verification: SUCCESS - Decryption matches original")
            return True
        else:
            print("Verification: FAILED - Decryption does not match original")
            return False

    except Exception as e:
        print("Verification error:", e)
        return False


# ============================================================
# MAIN PROGRAM
# ============================================================
# Flow:
#   1. Get user input (shift1, shift2)
#   2. Encrypt raw_text.txt
#   3. Decrypt encrypted_text.txt
#   4. Verify correctness
# ============================================================

def main():
    try:
        shift1 = int(input("Enter shift1: "))
        shift2 = int(input("Enter shift2: "))
    except ValueError:
        print("Invalid input. Please enter integers.")
        return

    input_file = "raw_text.txt"
    encrypted_file = "encrypted_text.txt"
    decrypted_file = "decrypted_text.txt"

    # Step 1: Encrypt
    encrypt_file(input_file, encrypted_file, shift1, shift2)
    print("Encryption complete.")

    # Step 2: Decrypt
    decrypt_file(encrypted_file, decrypted_file, shift1, shift2)
    print("Decryption complete.")

    # Step 3: Verify
    verify_files(input_file, decrypted_file)


if __name__ == "__main__":
    main()