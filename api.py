import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from models import User, Service, session


def create_user(username: str, password: str):
    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    user = User(
        username=username,
        key=base64.urlsafe_b64encode(kdf.derive(password.encode())),
        salt=base64.b64encode(salt).decode()
    )

    session.add(user)
    session.commit()


def get_user(username: str):
    return session.query(User).filter_by(username=username).first()


def check_password(username, password):
    user: User = session.query(User).filter_by(username=username).first()

    if user is None:
        return False

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=base64.b64decode(user.salt.encode()),
        iterations=100000,
        backend=default_backend()
    )

    return user.key == base64.urlsafe_b64encode(kdf.derive(password.encode()))


def add_service(user: User, service_name, service_username, service_password):
    f = Fernet(user.key)

    service = Service(
        user_id=user.id,
        service_name=service_name,
        username=service_username,
        password_hash=f.encrypt(service_password.encode()).decode()
    )

    session.add(service)
    session.commit()


def get_services():
    return session.query(Service)


def get_password(user: User, service_name):
    service: Service = session.query(Service).filter_by(service_name=service_name).first()

    f = Fernet(user.key)

    return f.decrypt(service.password_hash.encode()).decode()
