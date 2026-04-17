# Question 1 – Encryption & Decryption System Documentation

---

# 1. Overview

This program implements a **custom symmetric encryption system** for text files.

It reads raw text from a file (`raw_text.txt`), encrypts it using a rule-based alphabet shifting method, writes the encrypted result to `encrypted_text.txt`, then decrypts it back into `decrypted_text.txt`, and verifies correctness.

The system ensures that:

- Every encryption step is reversible
- Original data can always be recovered
- Non-alphabet characters remain unchanged

---

# 2. What the Program Represents

This program models a **simple substitution cipher system** with structured constraints:

- The English alphabet is divided into two independent groups:
  - Group 1: a–m / A–M
  - Group 2: n–z / N–Z

Each group behaves like a **separate modular system (mod 13 arithmetic)**.

👉 Conceptually, it represents:

> A controlled encryption system using segmented modular arithmetic.

---

# 3. Core Idea

Instead of using a single 26-letter rotation, the program:

- Splits alphabet into two halves
- Applies different transformation rules to each half
- Uses modulo 13 to keep transformations reversible

This ensures:
✔ no character escapes its group  
✔ encryption is reversible  
✔ structure is preserved

---

# 4. Encryption Logic

For each character:

## Lowercase letters:

- a–m → shift forward by (shift1 × shift2)
- n–z → shift backward by (shift1 + shift2)

## Uppercase letters:

- A–M → shift backward by shift1
- N–Z → shift forward by (shift2²)

## Other characters:

- Remain unchanged (spaces, numbers, symbols, emojis)

---

# 5. Decryption Logic

Decryption applies the **inverse operations** of encryption:

- Forward shifts become backward shifts
- Backward shifts become forward shifts
- Same grouping rules apply

This guarantees:

> Encryption → Decryption always restores original text

---

# 6. System Design

The program is structured into:

- File Handling Layer → reads/writes files
- Processing Layer → encryption/decryption logic
- Validation Layer → verification of correctness

This separation improves:
✔ readability  
✔ debugging  
✔ maintainability

---

# 7. Error Handling

The system handles:

- Missing files
- Empty input files
- Invalid user input
- Non-alphabet characters (ignored safely)

No program crash occurs under normal misuse conditions.

---

# 8. Output Files

| File               | Purpose                |
| ------------------ | ---------------------- |
| raw_text.txt       | Original input         |
| encrypted_text.txt | Encrypted output       |
| decrypted_text.txt | Restored original text |

---

# 9. Assumptions

- Only English alphabet is transformed
- Shift values are integers
- Characters outside A–Z / a–z are not modified

---

# 10. Key Properties

✔ Symmetric encryption (reversible)  
✔ Deterministic output  
✔ Structure-preserving transformation  
✔ Safe for mixed text input

---

# 11. How It Works (Pipeline)

1. Read file
2. Encrypt text
3. Save encrypted output
4. Read encrypted file
5. Decrypt text
6. Compare with original
7. Output verification result
