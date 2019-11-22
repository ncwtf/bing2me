### 自动更新win10壁纸

* Python3.7, sqlite
* 采集必应首页图片，设置为桌面壁纸
* 待完成列表 [TODO.md](https://github.com/ncwtf/bing2me/blob/master/TODO.md)

> 目录结构
```
│  bing2me.db
│  README.md
│  TODO.md
├─bing-pic
├─icons
├─src
│  │  bing_request.py
│  │  common.py
│  │  database.py
│  │  main.py
│  │  util.py
│  │  bing2me.py
|  |  log.py
└─test
      request.py
```

> python 运行时所需要的包
* pip install pywin32
  * 需要把win32文件夹两个DLL文件复制到 Windows/system32
* pip install requests
* pip install image
* pip install pillow
* pip install pyinstaller

> 问题记录
* 打包exe时需指定ssl的目录到环境变量
  * /python-path/DLLs
* pyinstaller -w -i=icons/panda.ico src/bing2me.py
* pyinstaller -w -F -i=icons/panda.ico src/bing2me.py
