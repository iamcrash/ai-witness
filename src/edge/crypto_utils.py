import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

class CryptoManager:
    @staticmethod
    def generate_sha256_hash(data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    @staticmethod
    def generate_key_pair():
        return rsa.generate_private_key(public_exponent=65537, key_size=2048)

    @staticmethod
    def sign_data(private_key, data: str) -> str:
        signature = private_key.sign(
            data.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return signature.hex()

    # EKSİK OLAN FONKSİYON BURASI:
    @staticmethod
    def verify_signature(public_key, signature_hex: str, data: str) -> bool:
        try:
            public_key.verify(
                bytes.fromhex(signature_hex),
                data.encode(),
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False