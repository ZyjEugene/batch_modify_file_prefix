# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


##!/usr/bin/env python
##coding=utf-8
import os
import sys
import re

# XY_ : 枚举值前缀
# XYY_ : 文件名前缀
# XYX_ : SDK暴露的头文件名前缀
# XYM_ : 用户登陆、内购、订单信息模型

# 第一步，要更改前缀是XY_文件的为XYY_前缀。
# 第二步，更改SDK暴露接口文件的前缀(XYX_)。
# 第三步，更改XY_枚举值前缀（全局匹配）。
# 第四步，更改XYY_文件名前缀。
# 第五步，更改XYM_文件名前缀（可选）。

# 需要修改的‘类名’前缀(需要替换)
pre_str = ''
# 新的‘类名’前缀(需要替换)
pre_to_str = ''

# 需要修改的文件中‘字符串’前缀(需要替换)
pre_var_str = 'XY_'
# 新的文件中‘字符串’前缀(需要替换)
pre_to_var_str = 'Ymx_'

# 需要修改的‘图片名’前缀(需要替换)
pre_pic_str = 'XYYI_'
# 新的‘图片名’前缀(需要替换)
pre_to_pic_str = 'Ymxi_'

# 搜寻以下文件类型(自己需要替换) , '.nib'
suf_set = ('.h', '.m', '.xib', '.storyboard', '.mm', '.pch', '.swift')
pic_suf_set = ('.png', '.jpg')

# 工程项目根路径(需要替换)
project_path = '/Users/yanjin/Desktop/YanJin-Workspace/Temp/XYSDK'

# 定义一个字典 key=旧类名 value=新类名
needModifyDic = {}
pbxprojFileAry = []
# 要修改的文件前缀 {pre_str : pre_to_str}
prefixDic = {'XY_':'XYY_'}
# prefixDic = {'XY_':'Ymx_',
#              'XYX_':'Ymx_',
#              'XYY_':'Ymx_',
#              'XYM_':'Ymx_'}

# 文件重命名函数，返回新的文件名
def file_rename(file_path):
    root_path = os.path.split(file_path)[0]     # 文件目录
    root_name = os.path.split(file_path)[1]     # 文件名包含扩展名
    filename = os.path.splitext(root_name)[0]  # 文件名
    filetype = os.path.splitext(root_name)[1]  # 文件扩展名

    new_file_name = filename.replace(pre_str, pre_to_str)
    if filetype in pic_suf_set:
        new_file_name = filename.replace(pre_pic_str, pre_to_pic_str)

    new_path = os.path.join(root_path, new_file_name + filetype)  # 拼接新路径
    os.renames(file_path, new_path)             # 文件重命名
    print('⚠️ %s --To--> %s' % (filename, new_file_name))
    return new_file_name

def rename_file(root, file_name):
    # 指定前、后缀，匹配具体范围的文件
    file_suf_set = suf_set + ('.nib', '.plist',)
    if (file_name.startswith((pre_str,)) and file_name.endswith(file_suf_set)) or \
            (file_name.startswith((pre_pic_str,)) and file_name.endswith(pic_suf_set)):
        print('file_name: %s' % file_name)
        old_name = os.path.splitext(file_name)[0]
        new_name = file_rename(os.path.join(root, file_name))
        needModifyDic[old_name] = new_name

# 修改项目中文件的前缀
def modify_file_prefix(project_path):
    for (root, dirs, files) in os.walk(project_path):
        # print('root : %s ' % root)
        # 修改nib文件（有些nib是个文件夹）
        for dir_name in dirs:
            filetype = os.path.splitext(dir_name)[1]
            if filetype == '.xcodeproj':
                # 项目配置文件路径(需要替换)(显示包内容 app.xcodeproj，找到project.pbxproj)
                # 项目配置文件路径拼接，为了更新重命名后 配置文件中的 ‘旧文件名’ 为 ‘新文件名’
                pbxproj = root + '/' + dir_name + '/project.pbxproj'
                pbxprojFileAry.append(pbxproj)
                print('xcodeproj_name: %s -> %s' % (dir_name, pbxproj))
            elif filetype in ('.xib', '.nib'):
                # 可视化文件重命名，修改nib文件（有些nib是个文件夹）
                rename_file(root, dir_name)

        # 修改普通文件
        for file_name in files:
            rename_file(root, file_name)

# 更新替换project.pbxproj配置文件中的类名
def modify_pbxproj_file(pbxproj_file):
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
def update_file_name(file_name, root):
    if file_name.endswith(suf_set):
        # print('-----fileName ： %s-------' % file_name)
        with open(os.path.join(root, file_name), 'r+') as f:
            s0 = f.read()
            f.close()
            for key in needModifyDic:
                if key in s0:
                    with open(os.path.join(root, file_name), 'r+') as f4:
                        s1 = f4.read().replace(key, needModifyDic[key])
                        print('update ' + key + ' --To--> ' + needModifyDic[key])
                        f4.seek(0)
                        f4.write(s1)
                        f4.truncate()
                        f4.close()

# 对文件中，符合规则的 “常量” 进行前缀的重命名（匹配替换）
def rename_var_prefix(file_name, root):
    if file_name.endswith(suf_set):
        with open(os.path.join(root, file_name), 'r+') as f4:
            s1 = f4.read()
            # \b 匹配单词的边界， 若 pre_str = 'XY_',则 TXY_、xy_格式的不会被匹配到
            s1 = re.sub(r'\b%s' % pre_var_str, pre_to_var_str, s1)
            f4.seek(0)
            f4.write(s1)
            f4.truncate()
            f4.close()

def main():
    print('-------- 💡 1、修改文件名（前缀）---------')
    modify_file_prefix(project_path)

    print('-------- 💡 2、修改配置文件---------')
    print(pbxprojFileAry)
    for file in pbxprojFileAry:
        print('修改配置文件: %s ' % file)
        modify_pbxproj_file(file)

    print('-------- 💡 3、文件重命名后，更换新类名的引用 ---------')
    print('符合重命名规则的文件如下：')
    print(needModifyDic)
    # 遍历文件，在文件中更换 "新类名" 的引用
    if len(needModifyDic) > 0:
        for (root, dirs, files) in os.walk(project_path):
            for file_name in files:
                update_file_name(file_name, root)

    print('-------- 💡 4、遍历所有文件，对文件中符合规则的 “字符串” 进行前缀的重命名（匹配替换） ---------')
    # 遍历文件，对符合规则的 “常量” 进行前缀的重命名（匹配替换）
    for (root, dirs, files) in os.walk(project_path):
        for file_name in files:
            rename_var_prefix(file_name, root)

    print('-------- 🏅 5、 Successful 🏅 --------')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # \b 匹配单词的边界 匹配替换结果：'TXY_TT HJQJ_TT xx xy HJQJ_ xy_'
    # str = re.sub(r'\b%s' % pre_str, pre_to_str, 'TXY_TT XY_TT xx xy XY_ xy_')

    if len(sys.argv) > 1:
        project_path = sys.argv[1]

    if not os.path.exists(project_path):
        print('》》请确认项目路径《《')

    for key, value in prefixDic.items():
        pre_str = key
        pre_to_str = value
        # 重命名文件前缀
        if len(pre_str) > 0 and len(pre_to_str) > 0:
            main()


#⚠️ 项目中的bundle文件要重新build，然后替换，否则可能会出现xib加载失败的问题！（具体原因暂未查明）