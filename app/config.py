'''
from jwcrypto.jwk import JWK
from jwcrypto.common import base64url_encode

class Config:
    SECRET_KEY = "9b9196e1691113bc0cab6fe5036f6bab38cb5c45dad9f5107587223a9bc7ec8caeb1c292f1ddcee5a47486f3d0fc4cd8f0040ac79f155575cc2eafb61522303f8c8421f45b7c4004f41980906fbc96c953b2cb424fba146ae30a854fbb69c605289e81dc331d83025e7e8731d6622b520ef6ef43bebe22827abea89320b0b8de"
    SQLALCHEMY_DATABASE_URI = "sqlite:///main.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_EXPIRY_TIME_IN_SECONDS = 60 * 60 * 24 * 14
    
    JWK = JWK(kid=1, kty="oct", alg="A128KW", enc="A128GCM", k=base64url_encode(SECRET_KEY[:16]))
    UPLOAD_FOLDER = '/static/productsDB'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = "environmeet@gmail.com"
    MAIL_PASSWORD = f"rohanaldomcDONALDO4927"
    MAIL_DEFAULT_SENDER = "environmeet@gmail.com"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
'''