from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

# Generate a private key
private_key = ec.generate_private_key(ec.SECP256R1())

# Generate the public key from the private key
public_key = private_key.public_key()

# Convert keys to the appropriate formats
def encode_key(key):
    return base64.urlsafe_b64encode(key).rstrip(b'=').decode('utf-8')

# Serialize the public key to bytes and then to Base64
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)
public_key_base64 = encode_key(public_key_bytes)

# Serialize the private key to bytes and then to Base64
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.DER,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
private_key_base64 = encode_key(private_key_bytes)

print("Public Key:", public_key_base64)
print("Private Key:", private_key_base64)