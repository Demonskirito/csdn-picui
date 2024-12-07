import os
import re
import json
import time
import uuid
import base64
import requests
from io import BytesIO
from requests_toolbelt.multipart.encoder import MultipartEncoder

from configs import CSDN_config, Setting_config
import chrome_src


class CSDNConvert(CSDN_config):
    """
    CSDN convert apply
    """
    def __init__(self, root):
        self.root = root
        self.chrome = chrome_src

        def get_short_id():
            """
            get a uuid form array
            :return: uuid form short id
            """
            # support .jpg .gif .png .jpeg .bmp .webp, size less than 5 Mb
            array = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                     "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                     "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                     "S", "T", "U", "V", "W", "X", "Y", "Z"]
            id_str = str(uuid.uuid4()).replace("-", '')
            buffer = []

            for i in range(0, 8):
                start = i * 4
                end = i * 4 + 4
                val = int(id_str[start:end], 16)
                buffer.append(array[val % 62])

            return "".join(buffer)

        self.fields.update({'uuid': 'img-' + get_short_id() + '-' + str(round(time.time() * 1000))})

    def convert(self, src):
        # convert address
        if src.find('http') >= 0:
            self.fields.update({'imgUrl': src})
            payload = json.dumps(self.fields)
            res = requests.post(self.convert_url, data=payload, cookies=self.cookies, headers=self.headers)
        # upload imgs and get address
        else:
            self.up_headers['x-image-suffix'] = src.split('.')[-1]
            up_res = requests.get(self.up_url, cookies=self.cookies, headers=self.up_headers).json()
            # if request legal
            if up_res['code'] != 200:
                self.chrome.start_chrome()  # 更新cookie
                return self.convert(src)
                #raise Exception(up_res['msg'])

            up_res = up_res['data']
            data = {
                'key': up_res['filePath'],
                'policy': up_res['policy'],
                'OSSAccessKeyId': up_res['accessId'],
                'signature': up_res['signature'],
                'callback': up_res['callbackUrl'],
                'file': open(os.path.join(self.root, src), 'rb').read()
            }
            multipart_encoder = MultipartEncoder(fields=data, boundary=self.boundary)
            res = requests.post(self.path_url, data=multipart_encoder, cookies=self.cookies, headers=self.path_headers)

        # if request legal
        if res.json()['code'] != 200:
            self.chrome.start_chrome()  # 更新cookie
            return self.convert(src)
            #raise Exception(res.json()['msg'])
        res_url = res.json()['data']['url'] if src.find('http') >= 0 else res.json()['data']['imageUrl']

        return res_url

def img_convert(text, root, link=False):
    handle = CSDNConvert(root)

    if link:
        res_url = handle.convert(text)
        # if get available convert address
        if not res_url:
            raise Exception('Convert false!')
        return res_url

    else:
        res_text = ''
        last_end = 0
        for query in re.finditer(Setting_config.pattern, text, re.I):
            src = query.group()[2:-1]
            print(f"{src}", end=' ')
            res_url = handle.convert(src)
            # if get available convert address
            if not res_url:
                raise Exception('Convert false!')
            # change source file, then do another search
            res_text += text[last_end:query.start() + 2] + res_url
            last_end = query.end() - 1
        res_text += text[last_end:]

        return res_text
