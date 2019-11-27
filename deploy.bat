@echo off
:::start
pyinstaller -y -w -i=icons/panda.ico src/bing2me.py
pyinstaller -y -w -F -i=icons/panda.ico src/bing2me.py

z:zip.exe -r ./dist/bing2me.zip ./dist/bing2me
::pause