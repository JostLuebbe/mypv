import sys
from PySide2 import QtWidgets

from views import LoginWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec_())

# p1: Password = session.query(Password).first()
#
# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=base64.b64decode(str.encode(p1.salt)),
#     iterations=100000,
#     backend=default_backend()
# )
#
# key = base64.urlsafe_b64encode(kdf.derive(b'some_password'))
# f = Fernet(key)
# print(f.decrypt(str.encode(p1.password_hash)))

# salt = os.urandom(16)
#
# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt=salt,
#     iterations=100000,
#     backend=default_backend()
# )
#
# key = base64.urlsafe_b64encode(kdf.derive(b'some_password'))
# f = Fernet(key)
# token = f.encrypt(b'some_other_password')
#
# p1 = Password(
#     service_name='Some Service',
#     username='user_name',
#     password_hash=token.decode(),
#     salt=base64.b64encode(salt).decode()
# )
# session.add(p1)
# session.commit()