import os

import pgpy
from pgpy import PGPKey
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm
from typing import Any
from warnings import filterwarnings

filterwarnings("ignore")


class PGPUtils:

    KEYS_FILE: str = f'{os.path.dirname(os.path.realpath(__file__))}/keys/keystore'

    @staticmethod
    def generate_key_pair():
        """
        A function that generates public and private keys.
        """

        pgp_key: PGPKey = pgpy.PGPKey.new(key_algorithm=PubKeyAlgorithm.RSAEncryptOrSign,
                                          key_size=4096)

        uid = pgpy.PGPUID.new(pn='Abraham Lincoln',
                              comment='Honest Abe',
                              email='abraham.lincoln@whitehouse.gov')
        pgp_key.add_uid(uid,
                        usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
                        hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA384, HashAlgorithm.SHA512, HashAlgorithm.SHA224],
                        ciphers=[SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192, SymmetricKeyAlgorithm.AES128],
                        compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP,
                                     CompressionAlgorithm.Uncompressed])
        return pgp_key

    @staticmethod
    def store_key(file_path: str,
                  key_pair: PGPKey):
        with open(file_path, "w") as key_store_file:
            key_store_file.write(str(key_pair))

    @staticmethod
    def load_key(file_path: str = KEYS_FILE) -> PGPKey:
        key, _ = pgpy.PGPKey.from_file(file_path)
        return key

    @staticmethod
    def encrypt(key: PGPKey, raw_data: Any) -> bytes:
        """
        Encrypts data with a key.
        """

        message = pgpy.PGPMessage.new(raw_data)
        enc_message = key.pubkey.encrypt(message)
        return bytes(enc_message)

    @staticmethod
    def decrypt(key: PGPKey, encrypted_data: bytes) -> str:
        """
        Decrypts data using a key.
        """

        message = pgpy.PGPMessage.from_blob(encrypted_data)
        return str(key.decrypt(message).message)


if __name__ == '__main__':
    key: PGPKey = PGPUtils.generate_key_pair()
    PGPUtils.store_key(PGPUtils.KEYS_FILE, key)
