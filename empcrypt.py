#!/usr/bin/env python3
import ctypes
import os
import sys

# Try to load local lib
LIB_PATHS = [
    "./libempcrypt.so",
    os.path.join(os.path.dirname(__file__), "libempcrypt.so")
]

def load_library():
    lib_path = next((p for p in LIB_PATHS if os.path.exists(p)), None)
    
    if not lib_path:
        print("Error: libempcrypt.so not found.")
        print("Run 'make' to compile the core library.")
        sys.exit(1)

    try:
        lib = ctypes.CDLL(lib_path)
        
        lib.EmpCrypt_Encrypt.argtypes = [ctypes.c_char_p]
        lib.EmpCrypt_Encrypt.restype = ctypes.c_void_p
        
        lib.EmpCrypt_Decrypt.argtypes = [ctypes.c_char_p]
        lib.EmpCrypt_Decrypt.restype = ctypes.c_void_p
        
        lib.free_string.argtypes = [ctypes.c_void_p]
        lib.free_string.restype = None
        
        return lib
    except OSError as e:
        print(f"Failed to load library: {e}")
        sys.exit(1)

def encrypt(text):
    lib = load_library()
    b_text = text.encode('utf-8')
    res_ptr = lib.EmpCrypt_Encrypt(b_text)
    
    if not res_ptr:
        return None
        
    try:
        return ctypes.cast(res_ptr, ctypes.c_char_p).value.decode('utf-8')
    finally:
        lib.free_string(res_ptr)

def decrypt(hex_text):
    lib = load_library()
    b_text = hex_text.encode('utf-8')
    res_ptr = lib.EmpCrypt_Decrypt(b_text)
    
    if not res_ptr:
        return None
        
    try:
        return ctypes.cast(res_ptr, ctypes.c_char_p).value.decode('utf-8')
    finally:
        lib.free_string(res_ptr)

def main():
    if len(sys.argv) < 3:
        print("Matrix42 EmpCrypt Python Port")
        print("Usage:")
        print("  python3 empcrypt.py encrypt <password>")
        print("  python3 empcrypt.py decrypt <hash>")
        sys.exit(1)

    action = sys.argv[1].lower()
    payload = sys.argv[2]

    if action.startswith("enc"):
        res = encrypt(payload)
        if res:
            print(res)
        else:
            print("Error: Encryption failed", file=sys.stderr)
            sys.exit(1)
            
    elif action.startswith("dec"):
        res = decrypt(payload)
        if res:
            print(res)
        else:
            print("Error: Decryption failed", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Unknown command: {action}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
