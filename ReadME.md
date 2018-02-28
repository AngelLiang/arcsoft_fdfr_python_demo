# Python调用虹软DLL库示例

forked from [asdfqwrasdf/ArcSoft_FreeSDK_Demo/FR/python/](https://github.com/asdfqwrasdf/ArcSoft_FreeSDK_Demo/tree/master/FR/python)

基于上面代码进行修改。

# 已测试过的环境

- CentOS 7.2 x64 + Python 3.5 
- Windows 10 x64 + Python 3.5（32bit）

注意事项：在Windows环境下，由于虹软DLL是32bit，所以Python必须也要32bit。

# 第一步：安装依赖包

首先需要安装依赖包（也就一个Pillow）

```sh
pip install -r requirements.txt
# OR
pip install Pillow
```

# 第二步：导入库文件

然后将虹软SDK中的DLL拷贝到`arcsoft\lib\`相关目录下，确保相关系统有detection和recognition两个库文件：

![lib](screenshot/lib.png)

# 第三步：填写信息

填写APPID、FD_SDKKEY和FR_SDKKEY。

```Python
APPID = c_char_p(b'APPID')
FD_SDKKEY = c_char_p(b'FD_SDKKEY')
FR_SDKKEY = c_char_p(b'FR_SDKKEY')
```

# 完成：运行测试

执行`python3 AFRTest.py`，成功的话会输出下面信息：

```sh
$ python3 AFRTest.py
#####################################################
0 1 0 87
ArcSoft_FreeSDK_Face_Detection_1.0.0.87
Dec 18 2017
Copyright 2017 ArcSoft, Inc. All rights reserved.
0 1 0 87
ArcSoft_FreeSDK_Face_Recognition_1.0.0.87
Dec 18 2017
Copyright 2017 ArcSoft, Inc. All rights reserved.
similarity between faceA and faceB is c_float(1.0)
#####################################################
```

# 修改输入图片

可以在`AFRTest.py`290行修改要输入的图片

```Python
# AFRTest.py 290行
filePathA = u'lena.bmp'
filePathB = u'lena.bmp'

inputImgA = loadImage(filePathA)
inputImgB = loadImage(filePathB)
```



