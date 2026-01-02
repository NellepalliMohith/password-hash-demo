# Password Hash Strength Demonstrator

A Python-based application that demonstrates how weak password hashing algorithms
and poor password choices can be vulnerable to brute-force and dictionary-based attacks.

This project is intended to **illustrate password security concepts**, not to attack
real systems.

---

## Features
- Supports **MD5, SHA-1, and NTLM** hashing
- Brute-force password demonstration (bounded for safety)
- Dictionary-based password demonstration
- Simple PyQt5 graphical interface
- Fast and predictable demo for interviews and learning

---

## Technologies Used
- Python 3
- PyQt5
- hashlib
- itertools
- PyInstaller (for executable build)

---

## How It Works

### Brute Force Demo
- Systematically generates password combinations
- Demonstrates how short and weak passwords can be recovered quickly
- Highlights exponential growth in search space as password length increases

### Dictionary Demo
- Tests hashes against common password lists
- Demonstrates risks of password reuse and weak credentials

---

## Example Demo (Recommended)
- Algorithm: MD5
- Password: `a1`
- Demonstrates successful brute-force recovery in under a second

---

## Disclaimer
This project is for **educational and security awareness purposes only**.
It should not be used against systems without explicit authorization.

---

## Author
Mohith
