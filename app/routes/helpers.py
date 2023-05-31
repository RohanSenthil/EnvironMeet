import os
import time
import json
from functools import wraps

from flask import session, abort, after_this_request, request, g, url_for
from jwcrypto.jwt import JWT

from app import app

#THANK YOU WEI TONG

def get_current_time_in_seconds():
    return int(time.time())

def get_token_expiry_time_from_now():
    return get_current_time_in_seconds() + app.config["TOKEN_EXPIRY_TIME_IN_SECONDS"]

def provide_new_login_token(user_id, permission_level):
    user_id = str(user_id)
    jwt = JWT(header={"kid": 1, "alg": "A128KW", "enc": "A128GCM"}, claims={"sub": user_id, "permission_level": permission_level, "exp": get_token_expiry_time_from_now()})
    jwt.make_encrypted_token(app.config["JWK"])
    jwt = jwt.serialize()

    @after_this_request
    def add_jwt_cookie(response):
        response.set_cookie("jwt", jwt)
        return response

def revoke_login_token():
    @after_this_request
    def remove_jwt_cookie(response):
        response.delete_cookie("jwt")
        return response

def refresh_login_token():
    provide_new_login_token(get_user_id_from_token(), get_user_permission_level_from_token())
    return True

def user_is_authenticated():
    if "jwt" in request.cookies and get_token_claims():
        return True
    else:
        return False

def get_token_claims():
    return json.loads(JWT(jwt=request.cookies["jwt"], key=app.config["JWK"], expected_type="JWE", algs=["A128KW", "A128GCM"], check_claims={"sub": None, "exp": None}).claims)

def get_user_id_from_token():
    return get_token_claims()["sub"]

def get_user_permission_level_from_token():
    return get_token_claims()["permission_level"]

def get_working_cart():
    if "ShoppingCart" in session:
        return session["ShoppingCart"]
    else:
        session["ShoppingCart"] = {}
        return session["ShoppingCart"]

def build_cart_key(product_id, colour):
    return json.dumps([product_id, colour])
app.add_template_global(build_cart_key)

def disassemble_cart_key(cart_key):
    return json.loads(cart_key)
app.add_template_global(disassemble_cart_key)

def update_cart():
    session.modified = True

def clear_cart():
    session["ShoppingCart"] = {}

def get_cart_value():
    cart = get_working_cart()
    cart_value = 0
    for product_id, product_dictionary in cart.items():
        cart_value += product_dictionary["quantity"] * product_dictionary["price"]
    return cart_value

def get_shipping_fee():
    cart_value = get_cart_value()
    if cart_value < 500:
        return 15
    else:
        return 0

def get_product_image_url(product):
    return url_for("static", filename=f"productsDB/{product.picture_1}")
app.add_template_global(get_product_image_url)

def privileged_route(permission_level):
    def wrapper(view_func):
        @wraps(view_func)
        def wrap(*args, **kwargs):
            if user_is_authenticated() and refresh_login_token() and get_user_permission_level_from_token() == permission_level:
                return view_func(*args, **kwargs)
            else:
                return abort(403)
        return wrap
    return wrapper

@app.before_request
def add_privilege_level():
    if "jwt" in request.cookies:
        g.privilege_level = get_user_permission_level_from_token()
    else:
        g.privilege_level = None
