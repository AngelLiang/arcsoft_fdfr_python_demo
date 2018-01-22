forked from [asdfqwrasdf/ArcSoft_FreeSDK_Demo/FR/python/](https://github.com/asdfqwrasdf/ArcSoft_FreeSDK_Demo/tree/master/FR/python)

# 第一步：安装依赖包

首先需要安装依赖包（也就一个Pillow）

```sh
pip install -r requirements.txt
```

OR

```sh
pip install Pillow
```

# 第二步：导入库文件

然后将虹软SDK中的lib目录直接拷贝到arcsoft目录下，确保有以下两个文件

- `arcsoft\lib\linux_x64\libarcsoft_fsdk_face_detection.so`
- `arcsoft\lib\linux_x64\libarcsoft_fsdk_face_recognition.so`

目前仅仅测试过Linux_x64下的Python3.5的调用，其它环境暂时未测试。

# 完成：运行测试

执行`AFRTest.py`，成功的话会输出下面信息：

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

可以在`AFRTest.py`244行修改要输入的图片

```Python
# AFRTest.py 244行
filePathA = u'lena.bmp'
filePathB = u'lena.bmp'

inputImgA = loadImage(filePathA)
inputImgB = loadImage(filePathB)
```



