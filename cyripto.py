from cryptography.fernet import Fernet
import os

class Crypto:
    def __init__(self):
        # This one going to be environment variable
        self.secretKey = os.getenv("SECRET_KEY")
        self.f = Fernet(self.secretKey)

    def password2secret(self,password):
        message = password.encode()
        return self.f.encrypt(message).decode("utf-8")

    def secret2password(self,secret):
        message = secret.encode()
        return self.f.decrypt(message)
