import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def start_chrome():
    try:
        # 设置Chrome浏览器的路径
        chrome_path = r'resources/chrome-win64/chrome.exe'
        chromedriver_path = r'resources/chrome-win64/chromedriver.exe'
        chrome_options = Options()
        chrome_options.binary_location = chrome_path  # 替换为您的Chrome路径
        service = Service(executable_path=chromedriver_path)  # 替换为您的chromedriver路径
        chrome_options.add_argument(r"user-data-dir=/tmp/")
        # 创建WebDriver实例
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('https://www.csdn.net/')# 打开网页
        time.sleep(2) # 等待网页加载完成

        while True:
            cookies = driver.get_cookies()
            user_info = {cookie['name']: cookie['value'] for cookie in cookies if
                         cookie['name'] in ['UserName', 'UserToken']}
            # 检查是否获取到了UserName和UserToken
            if 'UserName' in user_info and 'UserToken' in user_info:
                # 将UserName和UserToken写入cookies.json
                write_cookies(user_info)
                print('UserName和UserToken已保存到cookies.json')
                print(user_info)
                driver.quit()
                return True
            else:
                print('未获取到完整的cookie信息，等待1秒后重试...')
                time.sleep(1)

    except Exception as e:
        print("你似乎没有安装chrome或chromedriver，请先安装浏览器测试脚本。")
        print("Downlaod it from HERE：https://googlechromelabs.github.io/chrome-for-testing/#stable")
        print("修改chrome_src.py中start_chrome()函数的chrome_path和chromedriver_path后，再运行脚本。")

def write_cookies(user_info, json_file_path='cookies.json'):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # 如果文件不存在或文件内容不是有效的JSON格式，创建一个新的JSON对象
        data = {
              "default_modes": ["csdn"],
              "total_modes" : ["zhihu", "csdn", "bili", "jianshu", "bokeyuan"],
              "csdn_cookies" : {
                "UserName": "",
                "UserToken": ""
              },
              "zhihu_cookies": {
                "z_c0": ""
              },
              "bili_cookies": {
                "bili_jct": "",
                "SESSDATA": ""
              },
              "jianshu_cookies": {
                "remember_user_token": "",
                "_m7e_session_core": ""
              },
              "bokeyuan_cookies": {
                ".Cnblogs.AspNetCore.Cookies": ""
              }
            }

    # 更新csdn_cookies部分
    if 'UserName' in user_info and 'UserToken' in user_info:
        data['csdn_cookies']['UserName'] = user_info['UserName']
        data['csdn_cookies']['UserToken'] = user_info['UserToken']

        # 将更新后的数据写回JSON文件
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print('csdn_cookies部分已更新到cookies.json')
    else:
        print('未获取到完整的cookie信息，无法更新csdn_cookies部分。')
