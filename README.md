### 自动更新win10壁纸

* Python3.7, sqlite
* 采集必应首页图片，设置为桌面壁纸

> 目录结构
```
│  bing2me.db
│  README.md
│  TODO.md
├─bing-pic
├─src
│  │  bing2me.py
│  │  common.py
│  │  database.py
│  │  main.py
│  │  util.py
└─test
      request.py
```

> python 运行时所需要的包
* pip install pywin32
  * 需要把win32文件夹两个DLL文件复制到 Windows/system32
* pip install requests
* pip install image
* pip install pillow