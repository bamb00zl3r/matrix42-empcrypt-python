#include <dll.h>
#include <default.h>
#include <hex.h>
#include <filters.h>
#include <string>
#include <cstring>

using namespace CryptoPP;

/*
 * Extracted master key from EmpCrypt.exe
 * Algorithm: TripleDES-CBC + HMAC-SHA1 (LegacyEncryptorWithMAC)
 */
const byte MASTER_KEY[] = {
    0x1c, 0x69, 0xad, 0xe5, 0x24, 0x4d, 0x50, 0x4d,
    0x47, 0x5b, 0xd2, 0x79, 0x54, 0x8c, 0x75, 0xef,
    0x26, 0x44, 0xf7, 0x30, 0xa1, 0x4e, 0x15, 0x81
};

extern "C" {

    const char* EmpCrypt_Encrypt(const char* plaintext) {
        if (!plaintext) return nullptr;
        try {
            std::string cipher;
            // Uses LegacyEncryptorWithMAC -> TripleDES + SHA1 + MASH
            LegacyEncryptorWithMAC encryptor(MASTER_KEY, sizeof(MASTER_KEY), new HexEncoder(new StringSink(cipher)));
            encryptor.Put((byte*)plaintext, strlen(plaintext));
            encryptor.MessageEnd();

            char* result = new char[cipher.length() + 1];
            std::strcpy(result, cipher.c_str());
            return result;
        } catch (...) {
            return nullptr;
        }
    }

    const char* EmpCrypt_Decrypt(const char* hexCiphertext) {
        if (!hexCiphertext) return nullptr;
        try {
            std::string binaryCipher;
            StringSource(hexCiphertext, true, new HexDecoder(new StringSink(binaryCipher)));

            std::string recovered;
            LegacyDecryptorWithMAC decryptor(MASTER_KEY, sizeof(MASTER_KEY), new StringSink(recovered));
            decryptor.Put((byte*)binaryCipher.data(), binaryCipher.size());
            decryptor.MessageEnd();

            char* result = new char[recovered.length() + 1];
            std::strcpy(result, recovered.c_str());
            return result;
        } catch (...) {
            return nullptr;
        }
    }

    void free_string(char* str) {
        if (str) delete[] str;
    }
}
