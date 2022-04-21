from pages.models import Page
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import hashlib

# TODO: probably best to move to model


def verify_key(page_id, key):
    page_obj = Page.objects.get(uuid=page_id)
    return page_obj.hash == gen_hash(bytes(key, "utf-8"))

# TODO:MOVE TO MODEL
def decrypt_page(page_id, key):
    page_obj = Page.objects.get(uuid=page_id)
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(bytes(page_obj.template, "utf-8")).decode(
        "utf-8"
    )

# TODO;: MOVE TO MODEL
def get_derived_key(page_id, pwd):
    page_obj = Page.objects.get(uuid=page_id)
    password = bytes(pwd, "utf-8")
    salt = page_obj.salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    dk = base64.urlsafe_b64encode(kdf.derive(password))
    return dk


def gen_hash(key):
    h = hashlib.sha512()
    h.update(key)
    hsh = h.hexdigest()
    return hsh
