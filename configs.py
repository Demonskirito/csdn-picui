import json
import os
import sys

import chrome_src

path = os.path.join(os.path.split(os.path.abspath(sys.argv[0]))[0], "cookies.json")

''' loading json file '''

try:
    with open(path, 'r') as fp:
        dicts = json.loads(fp.read())
except Exception:
    print('Failed to read JSON file, attempting to start Chrome...')
    chrome_src.start_chrome()  # 执行chrome_src模块的start_chrome函数

# 检查是否达到最大尝试次数

""" include 4 modes, choose 1~4 as default mode(s) """
default_modes = dicts['default_modes']
total_modes = dicts['total_modes']

class Setting_config(object):
    """
        User can set your own parameters here
    """

    ''' config extensions which will be detected as pattern '''
    ''' (Warning!! some websites cannot support all extensions below) '''
    ext = ['png', 'bmp', 'jpg', 'jpeg', 'gif']
    pattern = ''.join(']\(?.*\.' + i + '\)|' + '="+.*\.' + i + '"|' for i in ext)[:-1]

    # csdn img-bed config
    csdn_cookies = dicts['csdn_cookies']
class CSDN_config(Setting_config):
    cookies = Setting_config.csdn_cookies

    up_headers = {
        'x-image-app': 'direct_blog',
        'x-image-dir': 'direct'
    }
    up_url = "https://imgservice.csdn.net/direct/v1.0/image/upload?watermark=&type=blog&rtype=markdown"

    boundary = '----WebKitFormBoundaryKzs0YGpR02NCBive'
    path_headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }
    path_url = "https://csdn-img-blog.oss-cn-beijing.aliyuncs.com/"

    fields = {'art_id': 'undefined'}
    cookies['UserInfo'] = cookies['UserToken']
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "content-type": "application/json"
    }
    convert_url = "https://imgservice.csdn.net/img-convert/external/storage"

