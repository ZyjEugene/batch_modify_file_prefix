# 工程项目文件前缀更新脚本

![](batch_file_terminal.png)
> XYSDK目前的文件结构
> 
> XY_ : 枚举值前缀 
> 
> XYY_ : 普通文件名前缀（也有一些前缀为XY_的，不多，就几个）
> 
> XYX_ : SDK暴露的头文件名前缀
> 
> XYM_ : 用户登陆、内购、订单信息模型
> 
> XYYI_ : 图片名前缀

### 脚本使用说明
````
1、更改脚本文件中的prefixDic字典，key为旧前缀，value为新前缀；

2、更改脚本文件中的project_path工程文件路径；

3、cd 脚本main.py文件所在的目录

4、执行以下命令即可
python3 main.py 
或  
python3 main.py 工程文件的根路径 # 更路径参数为可选，若添加了会覆盖脚本文件中的project_path

````

### 打包脚本
> 打包指令
> 
> ```$ pyinstaller -F main.py```
> 
> ⚠️打包失败报错：zsh: command not found: pyinstaller
> 
> ```$ pip3 install pyinstaller```

### 版本说明
> V1.0.0 完成测试初版（跑了一个测试项目，修改后能正常编译运行，是否有其他影响，还需要继续测试）
>
> V1.0.0 进行工程项目简单的测试。结果：⚠️ 项目中的bundle资源文件要重新build，然后替换；否则可能会出现xib加载失败的问题！（具体原因暂未查明）
> 
> V1.0.1 创建可视化用户界面（GUI），避免手动修改脚本内容
