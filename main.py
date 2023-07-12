# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


##!/usr/bin/env python
##coding=utf-8
__author__ = 'YanJin'

import os
import sys
import re
import time
import wx
from glob import glob

# XY_ : 枚举值前缀
# XYY_ : 文件名前缀
# XYX_ : SDK暴露的头文件名前缀
# XYM_ : 用户登陆、内购、订单信息模型

# 第一步，要更改前缀是XY_的文件前缀。
# 第二步，更改SDK暴露接口文件的前缀(XYX_)。
# 第三步，更改XY_枚举值前缀（全局匹配）。
# 第四步，更改XYY_文件名前缀。
# 第五步，更改XYM_文件名前缀（可选）。

# ---- 文件名 ----
# 需要修改的文件‘类名’前缀(需要替换)
pre_str = 'XY_'
# 新的文件‘类名’前缀(需要替换)
pre_to_str = 'XYY_'

# ---- 文件中的“字符串” ----
# 需要修改的文件中‘字符串’前缀(需要替换)，eg：枚举值前缀
pre_var_str = 'XY_'
# 新的文件中‘字符串’前缀(需要替换)
pre_to_var_str = 'Ymx_'

# ---- 图片名 ----
# 需要修改的‘图片名’前缀(需要替换)
pre_pic_str = 'XYYI_'
# 新的‘图片名’前缀(需要替换)
pre_to_pic_str = 'Ymxi_'

# ---- 脚本遍历的文件类型 ----
# 搜寻以下文件类型(自己需要替换)
suf_set = ('.h', '.m', '.xib', '.storyboard', '.mm', '.pch', '.swift')
pic_suf_set = ('.png', '.jpg')

# ---- 工程项目根路径(需要替换) ----
project_root_dir_path = "/Users/yanjin/Desktop/YanJin-Workspace/Temp/XYSDK_1"#'/Users/yanjin/Desktop/工程项目根目录'

# ---- 要修改的文件前缀 {pre_str : pre_to_str}，key：旧文件名前缀；value：新文件名前缀 ----
prefixDic = {'XY_':'XYY_'}
# prefixDic = {'XY_':'Ymx_',
#              'XYX_':'Ymx_',
#              'XYY_':'Ymx_',
#              'XYM_':'Ymx_'}

######## 👆使用前需要确认的内容👆 #########
 

# 定义一个字典 key=旧类名 value=新类名
needModifyDic = {}
pbxprojFileAry = []


# GUI的窗口尺寸
window_width = 550
window_height = 440
log_text_view = ""

def Log(msg):
    print(msg)
    log_text_view.AppendText(msg + "\n")

class BatchFile():
    def __init__(self, dir_root_path,callback):
        self.callback = callback
        self.main(dir_root_path)

    # 文件重命名函数，返回新的文件名
    def file_rename(self,file_path):
        root_path = os.path.split(file_path)[0]  # 文件目录
        root_name = os.path.split(file_path)[1]  # 文件名包含扩展名
        filename = os.path.splitext(root_name)[0]  # 文件名
        filetype = os.path.splitext(root_name)[1]  # 文件扩展名

        new_file_name = filename.replace(pre_str, pre_to_str)
        if filetype in pic_suf_set:
            new_file_name = filename.replace(pre_pic_str, pre_to_pic_str)

        new_path = os.path.join(root_path, new_file_name + filetype)  # 拼接新路径
        os.renames(file_path, new_path)  # 文件重命名
        if filename != new_file_name:
            Log('⚠️ %s --To--> %s' % (filename, new_file_name))

        return new_file_name

    def rename_file(self,root, file_name):
        # 指定前、后缀，匹配具体范围的文件
        file_suf_set = suf_set + ('.nib', '.plist',)
        if (file_name.startswith((pre_str,)) and file_name.endswith(file_suf_set)) or \
                (file_name.startswith((pre_pic_str,)) and file_name.endswith(pic_suf_set)):
            old_name = os.path.splitext(file_name)[0]
            new_name = self.file_rename(os.path.join(root, file_name))
            needModifyDic[old_name] = new_name

    # 修改项目中文件的前缀
    def modify_file_prefix(self,project_path):
        for (root, dirs, files) in os.walk(project_path):
            if not root.endswith(".*"):
                Log('root : %s' % root)
            # 修改nib文件（有些nib是个文件夹）
            for dir_name in dirs:
                filetype = os.path.splitext(dir_name)[1]
                if filetype == '.xcodeproj':
                    # 项目配置文件路径(需要替换)(显示包内容 app.xcodeproj，找到project.pbxproj)
                    # 项目配置文件路径拼接，为了更新重命名后 配置文件中的 ‘旧文件名’ 为 ‘新文件名’
                    pbxproj = root + '/' + dir_name + '/project.pbxproj'
                    pbxprojFileAry.append(pbxproj)
                    Log('xcodeproj_name: %s -> %s' % (dir_name, pbxproj))
                elif filetype in ('.xib', '.nib'):
                    # 可视化文件重命名，修改nib文件（有些nib是个文件夹）
                    self.rename_file(root, dir_name)

            # 修改普通文件
            for file_name in files:
                self.rename_file(root, file_name)

    # 更新替换project.pbxproj配置文件中的类名
    def modify_pbxproj_file(self,pbxproj_file):
        for key in needModifyDic:
            with open(pbxproj_file, 'r+') as f:
                s0 = f.read()
                f.close()
                if key in s0:
                    with open(pbxproj_file, 'r+') as f2:
                        s = f2.read().replace(key, needModifyDic[key])
                        f2.seek(0)
                        f2.write(s)
                        f2.truncate()
                        f2.close()

    # 遍历文件，在文件中更换 "新类名" 的引用
    def update_file_name(self, file_name, root):
        if file_name.endswith(suf_set):
            # Log('-----fileName ： %s-------' % file_name)
            with open(os.path.join(root, file_name), 'r+') as f:
                s0 = f.read()
                f.close()
                for key in needModifyDic:
                    if key in s0:
                        with open(os.path.join(root, file_name), 'r+') as f4:
                            s1 = f4.read().replace(key, needModifyDic[key])
                            if key != needModifyDic[key]:
                                Log('update ' + key + ' --To--> ' + needModifyDic[key])
                            f4.seek(0)
                            f4.write(s1)
                            f4.truncate()
                            f4.close()

    # 对文件中，符合规则的 “常量” 进行前缀的重命名（匹配替换）
    def rename_var_prefix(self, file_name, root):
        if file_name.endswith(suf_set):
            with open(os.path.join(root, file_name), 'r+') as f4:
                s1 = f4.read()
                # \b 匹配单词的边界， 若 pre_var_str = 'XY_',则 TXY_、xy_格式的不会被匹配到
                s1 = re.sub(r'\b%s' % pre_var_str, pre_to_var_str, s1)
                f4.seek(0)
                f4.write(s1)
                f4.truncate()
                f4.close()

    def main(self, project_path):
        Log('-------- 💡 1、修改文件名（前缀）---------')
        self.modify_file_prefix(project_path)

        Log('-------- 💡 2、修改配置文件---------')
        print(pbxprojFileAry)
        for file in pbxprojFileAry:
            Log('修改配置文件: %s ' % file)
            self.modify_pbxproj_file(file)

        Log('-------- 💡 3、文件重命名后，更换新类名的引用 ---------')
        Log('符合重命名规则的文件如下：')
        print(needModifyDic)
        # 遍历文件，在文件中更换 "新类名" 的引用
        if len(needModifyDic) > 0:
            for (root, dirs, files) in os.walk(project_path):
                for file_name in files:
                    self.update_file_name(file_name, root)

        Log('-------- 💡 4、遍历所有文件，对文件中符合规则的 “字符串” 进行前缀的重命名（匹配替换） ---------')
        # 遍历文件，对符合规则的 “常量” 进行前缀的重命名（匹配替换）
        for (root, dirs, files) in os.walk(project_path):
            for file_name in files:
                self.rename_var_prefix(file_name, root)

        Log('-------- 🏅 5、 Successful 🏅 --------')
        self.callback()


# Window GUI
Pro_Name = "BatchXXFilesPrefix"
class HelloFrame(wx.Frame):
    """
    A Frame that says Hello World
    """
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(HelloFrame, self).__init__(*args, **kw)

        self.makeUILayout()

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to " + Pro_Name + " !")

# ----- UI Layout -----
    def makeUILayout(self):
        panel = wx.Panel(self)

        fir_top = 10
        label = wx.StaticText(panel, label="Dir Path:", pos=(10, fir_top), size=(80, 35))
        self.tfview = wx.TextCtrl(panel, pos=(70, fir_top), size=(200, 20), style=wx.TE_RIGHT)
        btn = wx.Button(panel, label="Sel Dir", pos=(300, fir_top), size=(80, 20))
        btn.Bind(wx.EVT_BUTTON, self.OnClicked)

        sec_top = fir_top + 35
        pre_tip = wx.StaticText(panel, label="File Prefix From:", pos=(10, sec_top), size=(80, 35))
        self.pre_tfview = wx.TextCtrl(panel, pos=(125, sec_top), size=(60, 20), value=pre_str)
        sub_tip = wx.StaticText(panel, label="To:", pos=(190, sec_top), size=(30, 35))
        self.new_tfview = wx.TextCtrl(panel, pos=(220, sec_top), size=(60, 20), value=pre_to_str)

        third_top = sec_top + 35
        pre_tip = wx.StaticText(panel, label="Const Prefix From:", pos=(10, third_top), size=(80, 35))
        self.pre_const_tfview = wx.TextCtrl(panel, pos=(125, third_top), size=(60, 20), value=pre_var_str)
        sub_tip = wx.StaticText(panel, label="To:", pos=(190, third_top), size=(30, 35))
        self.new_const_tfview = wx.TextCtrl(panel, pos=(220, third_top), size=(60, 20), value=pre_to_var_str)

        for_top = third_top + 35
        pre_tip = wx.StaticText(panel, label="Image Prefix From:", pos=(10, for_top), size=(80, 35))
        self.pre_img_tfview = wx.TextCtrl(panel, pos=(125, for_top), size=(60, 20), value=pre_pic_str)
        sub_tip = wx.StaticText(panel, label="To:", pos=(190, for_top), size=(30, 35))
        self.new_img_tfview = wx.TextCtrl(panel, pos=(220, for_top), size=(60, 20), value=pre_to_pic_str)

        fiv_top = for_top + 30
        self.start_btn = wx.Button(panel, label="Start", pos=(300, fiv_top))
        self.start_btn.Bind(wx.EVT_BUTTON, self.OnStartClicked)

        six_top = fiv_top + 30
        self.onGoingText = wx.TextCtrl(panel, pos=(10, six_top), size=(window_width-20, 180), style=wx.TE_READONLY | wx.TE_MULTILINE)

        global log_text_view
        log_text_view = self.onGoingText

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(log_text_view, 0, wx.ALL|wx.EXPAND)

    # 事件回调
    def finish_callback(self):
        Log("-------- end --------")
        self.start_btn.SetLabel("Start")
        self.start_btn.Enable()

    def OnClicked(self, event):
        frame = wx.Frame(None, -1, 'win.py')
        # frame.SetDimensions(0, 0, 200, 50)

        openDirDialog = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if openDirDialog.ShowModal() == wx.ID_OK:
            self.tfview.Clear()
            self.tfview.SetValue(openDirDialog.GetPath())
            Log("📁Sel Dir Path: " + self.tfview.GetValue())

    def OnStartClicked(self, event):
        project_path = self.tfview.GetValue()
        if not os.path.exists(project_path):
            print()
            Log('》》请确认项目路径《《')
            return

        global pre_str
        global pre_to_str
        global pre_var_str
        global pre_to_var_str
        global pre_pic_str
        global pre_to_pic_str
        pre_str = self.pre_tfview.GetValue()
        pre_to_str = self.new_tfview.GetValue()

        pre_var_str = self.pre_const_tfview.GetValue()
        pre_to_var_str = self.new_const_tfview.GetValue()

        pre_pic_str = self.pre_img_tfview.GetValue()
        pre_to_pic_str = self.new_img_tfview.GetValue()

        Log("")
        Log("")
        Log("-- 👇prepare👇 --")
        Log("dir path:" + project_path)

        # 重命名文件前缀
        if len(pre_str) > 0 and len(pre_to_str) > 0:
            Log("-- start --")
            self.start_btn.SetLabel("Processing")
            self.start_btn.Disable()
            BatchFile(project_path, callback=self.finish_callback)
        else:
            Log("-- pre_str & pre_to_str are nil --")

# ----- Menu Bar ----
    def makeMenuBar(self):
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        menuBar = wx.MenuBar()
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a batch modify file prefix program",
                      "modify file prefix program",
                      wx.OK|wx.ICON_INFORMATION)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    app_frame = HelloFrame(None, wx.ID_ANY, title=Pro_Name, size=(window_width, window_height))

    app_frame.Show()
    app.MainLoop()


#⚠️ 项目中的bundle文件要重新build，然后替换，否则可能会出现xib加载失败的问题！（具体原因暂未查明）

# -- 参考资料
# [GUI工具包使用](https://www.wxpython.org/pages/overview/)
