import base64
import json
import time
import copy
import hmac


class TokenError(Exception):
    pass

class Jwt:
    @staticmethod
    def b64encode(content):
        return base64.urlsafe_b64encode(content).replace(b'=', b'')

    @staticmethod
    def b64decode(content):
        count = ""
        if len(content) > 0:
            count = '=' * (4 - (len(content) % 4))
        return base64.urlsafe_b64decode(content + count)

    @staticmethod
    def encode(payload, key, exp=300):
        # init header
        header = {'alg': 'HS256', 'typ': 'JWT'}
        header_json = json.dumps(header, sort_keys=True, separators=(",", ":"))
        header_b64 = Jwt.b64encode(header_json.encode())

        # init payload
        payload_self = copy.deepcopy(payload)
        if not isinstance(exp, int) and not isinstance(exp, str):
            raise TokenError('exp nust be int or str !')
        try:
            payload_self["exp"] = time.time() + int(exp)
        except:
            raise TokenError('exp nust be int !')

        payload_json = json.dumps(payload_self, sort_keys=True, separators=(",", ":"))
        payload_b64 = Jwt.b64encode(payload_json.encode())

        # init sign
        if isinstance(key, str):
            key = key.encode()

        hm = hmac.new(key, header_b64 + b'.' + payload_b64, digestmod='SHA256')

        sign_b64 = Jwt.b64encode(hm.digest())
        return header_b64 + b'.' + payload_b64 + b'.' + sign_b64

    @staticmethod
    def decode(token, key):
        if isinstance(token, str):
            token = token.encode()
        header_bs, payload_bs, sign_bs = token.decode().split(".")

        # init sign
        if isinstance(key, str):
            key = key.encode()

        hm = hmac.new(key, header_bs.encode() + b'.' + payload_bs.encode(), digestmod="SHA256")

        # 比对
        print(sign_bs.encode())
        print(Jwt.b64encode(hm.digest()))

        if Jwt.b64encode(hm.digest()) != sign_bs.encode():
            raise TokenError("签名不正确!")

        payload_js = Jwt.b64decode(payload_bs)
        payload_dic = json.loads(payload_js)
        if "exp" in payload_dic:
            now = time.time()
            if now > payload_dic["exp"]:
                raise TokenError("超时")

        return payload_dic


if __name__ == "__main__":
    j = Jwt.encode({"username": "guoxiaonao"}, '12345', 'aaa')

    print(j)

    print(Jwt.decode(j, '12345'))
