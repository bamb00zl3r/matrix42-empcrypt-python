# Matrix42 EmpCrypt Python Port

A native Python port of the Matrix42 EmpCrypt utility, allowing encryption and decryption of Empirum passwords on Linux without requiring Wine or the original Windows binaries.

## Overview

This project provides a Python CLI wrapper around a small C++ core (`libempcrypt.so`). It replicates the original encryption logic (TripleDES-CBC + HMAC-SHA1 using Crypto++'s legacy `DefaultEncryptorWithMAC`).

## Prerequisites

- Python 3.x
- `libcrypto++-dev` (required for compilation)

### Installing dependencies (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install libcrypto++-dev g++ make
```

## Compilation

Build the core shared library using the included Makefile:

```bash
make
```

This will produce `libempcrypt.so` in the current directory.

## Usage

Run the Python script directly:

### Encryption
```bash
python3 empcrypt.py encrypt "P@ssw0rd"
# Output: 4CC7FE0A2C9F92BA646E4F89775D8DC3F5C4CC3D1F65142565D0167E56E6929F4BBD5C6F129C8F33303E53141A6F31C1
```

### Decryption
```bash
python3 empcrypt.py decrypt "4CC7FE0A2C9F92BA646E4F89775D8DC3F5C4CC3D1F65142565D0167E56E6929F4BBD5C6F129C8F33303E53141A6F31C1"
# Output: P@ssw0rd
```

## Disclaimer

This project is for educational purposes only.
