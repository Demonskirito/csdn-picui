import webbrowser
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess
import os
import re
import convert


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

def open_browser(url):
    # 使用 webbrowser 模块在默认浏览器中打开 URL
    webbrowser.open(url)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        # 设置 uploads 文件夹的相对路径
        upload_folder = os.path.join('uploads')
        os.makedirs(upload_folder, exist_ok=True)  # 确保文件夹存在
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        print(file_path)


        try:
            # convert.exe 的相对路径
            root_path=os.getcwd()
            print("root_path:"+root_path)
            absolute_path = root_path +"\\"+ file_path
            print("absolute_path:"+absolute_path)
            result = convert.handler(absolute_path)
            print(result)

            # 提取生成的 URL
            url_match = re.search(r"https[^']*'", result)
            if url_match:
                url = url_match.group(0)[:-1]
                return jsonify({"url": url})
            else:
                return jsonify({"error": "URL not found in convert.exe output"}), 500

        except subprocess.CalledProcessError as e:
            # 输出错误信息
            print(f"Error executing convert.exe: {e.output}")
            return jsonify({"error": "Failed to execute convert.exe"}), 500

    return jsonify({"error": "No file uploaded"}), 400


if __name__ == '__main__':
    # 获取应用的 URL
    url = 'http://127.0.0.1:5000/'
    # 在新线程中打开浏览器，以免阻塞 Flask 应用的启动
    import threading
    threading.Timer(1, open_browser, [url]).start()
    # 启动 Flask 应用
    app.run(port=5000)
