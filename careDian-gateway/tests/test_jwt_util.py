from gateway.jwt_util import jwt_encode_hs256, jwt_decode_hs256, JWTError, claims_access
import time


def test_jwt_ok():
    s = "sec"
    tok = jwt_encode_hs256(claims_access("u", exp_sec=60, iss="i", aud="a"), s)
    assert jwt_decode_hs256(tok, s, iss="i", aud="a")["sub"] == "u"

def test_jwt_expired():
    s = "sec"
    tok = jwt_encode_hs256({"sub":"u","exp": int(time.time())-1}, s)
    
    try:
        jwt_decode_hs256(tok, s)
        assert False
    except JWTError:
        pass