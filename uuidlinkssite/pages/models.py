from django.db import models
import uuid
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import hashlib

# Create your models here.
class Page(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hash = models.CharField(max_length=128)
    salt = models.BinaryField()
    title = models.CharField(max_length=100)
    template = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        password = bytes(kwargs["password"], "utf-8")
        salt = os.urandom(32)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        h = hashlib.sha512()
        h.update(key)
        self.hash = h.hexdigest()
        self.salt = salt
        cipher_suite = Fernet(key)
        self.template = cipher_suite.encrypt(
            bytes(kwargs["template_block"], "utf-8")
        ).decode("utf-8")
        super().save()
