import jwt
import bcrypt
json = {
    "id": "justkode",
    "password": "password"
}
encoded = jwt.encode(json, "secret", algorithm="HS256")  # byte-string
decoded = jwt.decode(encoded, "secret", algorithm="HS256")  # dict

print(
    encoded)  # b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6Imp1c3Rrb2RlIiwicGFzc3dvcmQiOiJwYXNzd29yZCJ9.TKGlCElSgGthalfeTlbN_giphG9AC5y5HwCbz93N0cs'
print(decoded)  # {'id': 'justkode', 'password': 'password'}

