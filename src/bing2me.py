import win32api
import win32con
import win32gui_struct
import win32gui
import os
from tkinter import messagebox as mb
import util
import common
import database as db
import job
import log

Main = None
logger = log.LOGGER


class SysTrayIcon(object):
    QUIT = 'QUIT'
    BOOTUP = 'BOOTUP'
    CHANGE_WALLPAPER = 'CHANGE_WALLPAPER'
    SPECIAL_ACTIONS = [QUIT, BOOTUP, CHANGE_WALLPAPER]
    FIRST_ID = 1314

    def __init__(self,
                 icon,
                 hover_text,
                 menu_options,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name=None, ):
        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit

        logger.info(common.CHECK_MARK_ICO_PATH)
        menu_options += (
            ('开机启动', common.CHECK_MARK_ICO_PATH, self.BOOTUP),
            ('更换壁纸', None, self.CHANGE_WALLPAPER),
            ('退出', None, self.QUIT),
        )
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        del self._next_action_id

        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.refresh_icon,
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER + 20: self.notify, }
        # 注册窗口类。
        window_class = win32gui.WNDCLASS()
        window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map  # 也可以指定wndproc.
        self.classAtom = win32gui.RegisterClass(window_class)

    def show_icon(self):
        # 创建窗口。
        hinst = win32gui.GetModuleHandle(None)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(self.classAtom,
                                          self.window_class_name,
                                          style,
                                          0,
                                          0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0,
                                          0,
                                          hinst,
                                          None)
        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh_icon()

        win32gui.PumpMessages()

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)
        # win32gui.SetMenuDefaultItem(menu, 1000, 0)

        pos = win32gui.GetCursorPos()
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def destroy(self, hwnd, msg, wparam, lparam):
        if self.on_quit: self.on_quit(self)  # 运行传递的on_quit
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # 退出托盘图标

    def notify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK:  # 双击左键
            mb.showinfo("Oops", "Application is already running")
        elif lparam == win32con.WM_RBUTTONUP:  # 单击右键
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:  # 单击左键
            pass
        return True

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
            else:
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
            self._next_action_id += 1
        return result

    def refresh_icon(self, **data):
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon):  # 尝试找到自定义图标
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       self.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else:  # 找不到图标文件 - 使用默认值
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD
        self.notify_id = (self.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER + 20,
                          hicon,
                          self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_id in self.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        # 首先加载图标。
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # 填满背景。
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # "GetSysColorBrush返回缓存的画笔而不是分配新的画笔。"
        #  - 暗示没有DeleteObject
        # 画出图标
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def command(self, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        self.execute_menu_option(id)

    def execute_menu_option(self, id):
        menu_action = self.menu_actions_by_id[id]
        if menu_action == self.QUIT:
            win32gui.DestroyWindow(self.hwnd)
        elif menu_action == self.BOOTUP:
            # 设置开机自启逻辑
            boot_up = BootUp()
            # 获取当前开机自启状态
            boot_up_status = boot_up.status()
            mb_input = mb.askquestion(
                "设置开机启动",
                "当前 [%s] 开机启动, 是否变更状态?" % ("已设置" if boot_up_status else "未设置"),
            )
            if mb_input == "yes":
                boot_up.close() if boot_up_status else boot_up.open()
        elif menu_action == self.CHANGE_WALLPAPER:
            # 更换壁纸
            util.change_wallpaper()
            pass
        else:
            mb.showerror("error", "no action")


class BootUp:
    app_name = common.APP_NAME
    app_path = common.SYS_ARGV
    # 注册表项名
    key_name = r'Software\Microsoft\Windows\CurrentVersion\Run'

    def status(self):
        try:
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, self.key_name, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegQueryValueEx(key, self.app_name)
            win32api.RegCloseKey(key)
            logger.info(u'已设置开机自启')
            return True
        except:
            logger.info(u'未设置开机自启')
            return False

    def open(self):
        # 异常处理
        try:
            logger.info(u'设置开机自启...')
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, self.key_name, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, self.app_name, 0, win32con.REG_SZ, self.app_path)
            win32api.RegCloseKey(key)
        except:
            logger.warn(u'设置开机自启失败')

    def close(self):
        try:
            logger.info(u'关闭开机自启...')
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, self.key_name, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegDeleteValue(key, self.app_name)
            win32api.RegCloseKey(key)
        except:
            logger.warn(u'关闭开机自启失败')


class _Main:
    def __init__(self):
        # init
        logger.info(u'初始化数据库、图片文件夹')
        db.init()
        util.makedirs(common.BING_PIC_DIR)
        util.get_icons()
        # 检查是否多开
        util.suicider()
        # TODO 更换壁纸
        # util.change_wallpaper()
        job.Timing(1, "Thread-1", 1).start()

    def main(self):
        import tkinter as tk

        self.root = tk.Tk()
        logger.info(common.PANDA_ICO_PATH)
        hover_text = "bing2me\n每天自动更新壁纸\n(#^.^#)"  # 悬浮于图标上方时的提示
        menu_options = ()
        self.sysTrayIcon = SysTrayIcon(
            common.PANDA_ICO_PATH,
            hover_text,
            menu_options,
            on_quit=self.exit,
            default_menu_index=1
        )

        self.root.state("iconic")  # 直接设置为窗口隐藏
        self.root.bind("<Unmap>", lambda event: self.Unmap() if self.root.state() == 'iconic' else False)
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.root.resizable(0, 0)
        self.root.mainloop()

    def Unmap(self):
        self.root.withdraw()
        self.sysTrayIcon.show_icon()

    def exit(self, _sysTrayIcon=None):
        self.root.destroy()
        logger.info('exit...')


if __name__ == '__main__':
    log.LOG.logo()
    Main = _Main()
    Main.main()
