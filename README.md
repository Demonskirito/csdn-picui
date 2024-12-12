# CSDN图床使用说明


## 1.下载chrome浏览器内核

https://googlechromelabs.github.io/chrome-for-testing/#stable

分别下载chrome和chromedriver

![Pasted image 20241209132851](https://github.com/user-attachments/assets/ad89e9b6-8249-4c19-9de3-274150675047)


下载完后在chrome_src.py中去设置Chrome浏览器的路径

![Pasted image 20241209133055](https://github.com/user-attachments/assets/806a82ab-8052-4be1-bf44-82b6719aa4fa)


如果不想改的话可以参考我项目的结构去设置
![Pasted image 20241209192537](https://github.com/user-attachments/assets/eba268a1-f199-48a1-9eb9-e4d0cf151dd4)


配置好chrome.exe和chromedriver.exe的路径后我们就可以去使用当前项目了

## 2.启动项目

运行server.py，端口为127.0.0.1:5000;

启动项目后会跳出chrome浏览器并出现在csdn的首页，在这里我们直接登录csdn就可以获取到token存入cookie.josn

之后便会在你的默认浏览器跳出页面，祝贺你，你的csdn图床成功部署了



![Pasted image 20241209193339](https://github.com/user-attachments/assets/92d52304-4859-4758-80a8-01e20ca7c404)


在这里我们点击图片框我们就可以上传我们的照片至csdn的图床了

![Pasted image 20241209193444](https://github.com/user-attachments/assets/224f326a-ac02-4616-aa35-a05eb3a6747c)

csdn图床exe文件分享
https://1drv.ms/u/s!AmaP7qa1s2hZgQFO8yz9FC-mP5x0?e=xs6fX4
