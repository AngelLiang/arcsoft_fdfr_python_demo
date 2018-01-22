#-*- encoding=utf-8 -*-

from arcsoft import CLibrary, ASVL_COLOR_FORMAT, ASVLOFFSCREEN,c_ubyte_p,FaceInfo
from arcsoft.utils import BufferInfo, ImageLoader
from arcsoft.AFD_FSDKLibrary import *
from arcsoft.AFR_FSDKLibrary import *
from ctypes import *
import traceback

APPID = c_char_p(b'APPID')
FD_SDKKEY = c_char_p(b'FD_SDKKEY')
FR_SDKKEY = c_char_p(b'FR_SDKKEY')

FD_WORKBUF_SIZE = 20 * 1024 * 1024
FR_WORKBUF_SIZE = 40 * 1024 * 1024
MAX_FACE_NUM = 50

def doFaceDetection(hFDEngine, inputImg):
    faceInfo = []

    pFaceRes = POINTER(AFD_FSDK_FACERES)()
    ret = AFD_FSDK_StillImageFaceDetection(hFDEngine, byref(inputImg), byref(pFaceRes))
    if ret != 0:
        print(u'AFD_FSDK_StillImageFaceDetection 0x{0:x}'.format(ret))
        return faceInfo

    faceRes = pFaceRes.contents
    if faceRes.nFace > 0:
        for i in range(0, faceRes.nFace):
            rect = faceRes.rcFace[i]
            orient = faceRes.lfaceOrient[i]
            faceInfo.append(FaceInfo(rect.left,rect.top,rect.right,rect.bottom,orient))

    return faceInfo

def extractFRFeature(hFREngine, inputImg, faceInfo):
    """
    获取人脸特征值
    """
    faceinput = AFR_FSDK_FACEINPUT()
    faceinput.lOrient = faceInfo.orient
    faceinput.rcFace.left = faceInfo.left
    faceinput.rcFace.top = faceInfo.top
    faceinput.rcFace.right = faceInfo.right
    faceinput.rcFace.bottom = faceInfo.bottom

    faceFeature = AFR_FSDK_FACEMODEL()
    ret = AFR_FSDK_ExtractFRFeature(hFREngine, inputImg, faceinput, faceFeature)
    if ret != 0:
        print(u'AFR_FSDK_ExtractFRFeature ret 0x{0:x}'.format(ret))
        return None

    try:
        return faceFeature.deepCopy()
    except Exception as e:
        traceback.print_exc()
        print(e.message)
        return None


def compareFaceSimilarity(hFDEngine, hFREngine, inputImgA, inputImgB):
    """
    人脸相似度对比
    """
    # Do Face Detect
    faceInfosA = doFaceDetection(hFDEngine, inputImgA)
    if len(faceInfosA) < 1:
        print(u'no face in Image A ')
        return 0.0
    faceInfosB = doFaceDetection(hFDEngine, inputImgB)
    if len(faceInfosB) < 1:
        print(u'no face in Image B ')
        return 0.0

    # Extract Face Feature
    faceFeatureA = extractFRFeature(hFREngine, inputImgA, faceInfosA[0])
    if faceFeatureA == None:
        print(u'extract face feature in Image A faile')
        return 0.0
    faceFeatureB = extractFRFeature(hFREngine, inputImgB, faceInfosB[0])
    if faceFeatureB == None:
        print(u'extract face feature in Image B failed')
        faceFeatureA.freeUnmanaged()
        return 0.0

    # calc similarity between faceA and faceB
    fSimilScore = c_float(0.0)
    ret = AFR_FSDK_FacePairMatching(hFREngine, faceFeatureA, faceFeatureB, byref(fSimilScore))
    faceFeatureA.freeUnmanaged()
    faceFeatureB.freeUnmanaged()
    if ret != 0:
        print(u'AFR_FSDK_FacePairMatching failed:ret 0x{0:x}'.format(ret))
        return 0.0

    return fSimilScore

def loadYUVImage(yuv_filePath, yuv_width, yuv_height, yuv_format):
    """
    加载YUV图片
    """
    yuv_rawdata_size = 0

    inputImg = ASVLOFFSCREEN()
    inputImg.u32PixelArrayFormat = yuv_format
    inputImg.i32Width = yuv_width
    inputImg.i32Height = yuv_height
    if ASVL_COLOR_FORMAT.ASVL_PAF_I420 == inputImg.u32PixelArrayFormat:
        inputImg.pi32Pitch[0] = inputImg.i32Width
        inputImg.pi32Pitch[1] = inputImg.i32Width // 2
        inputImg.pi32Pitch[2] = inputImg.i32Width // 2
        yuv_rawdata_size = inputImg.i32Width * inputImg.i32Height * 3 // 2
    elif ASVL_COLOR_FORMAT.ASVL_PAF_NV12 == inputImg.u32PixelArrayFormat:
        inputImg.pi32Pitch[0] = inputImg.i32Width
        inputImg.pi32Pitch[1] = inputImg.i32Width
        yuv_rawdata_size = inputImg.i32Width * inputImg.i32Height * 3 // 2
    elif ASVL_COLOR_FORMAT.ASVL_PAF_NV21 == inputImg.u32PixelArrayFormat:
        inputImg.pi32Pitch[0] = inputImg.i32Width
        inputImg.pi32Pitch[1] = inputImg.i32Width
        yuv_rawdata_size = inputImg.i32Width * inputImg.i32Height * 3 // 2
    elif ASVL_COLOR_FORMAT.ASVL_PAF_YUYV == inputImg.u32PixelArrayFormat:
        inputImg.pi32Pitch[0] = inputImg.i32Width * 2
        yuv_rawdata_size = inputImg.i32Width * inputImg.i32Height * 2
    else:
        print(u'unsupported  yuv format')
        exit(0)

    # load YUV Image Data from File
    f = None
    try:
        f = open(yuv_filePath, u'rb')
        imagedata = f.read(yuv_rawdata_size)
    except Exception as e:
        traceback.print_exc()
        print(e.message)
        exit(0)
    finally:
        if f is not None:
            f.close()

    if ASVL_COLOR_FORMAT.ASVL_PAF_I420 == inputImg.u32PixelArrayFormat:
        inputImg.ppu8Plane[0] = cast(imagedata, c_ubyte_p)
        inputImg.ppu8Plane[1] = cast(addressof(inputImg.ppu8Plane[0].contents) + (inputImg.pi32Pitch[0] * inputImg.i32Height), c_ubyte_p)
        inputImg.ppu8Plane[2] = cast(addressof(inputImg.ppu8Plane[1].contents) + (inputImg.pi32Pitch[1] * inputImg.i32Height // 2), c_ubyte_p)
        inputImg.ppu8Plane[3] = cast(0, c_ubyte_p)
    elif ASVL_COLOR_FORMAT.ASVL_PAF_NV12 == inputImg.u32PixelArrayFormat:
        inputImg.ppu8Plane[0] = cast(imagedata, c_ubyte_p)
        inputImg.ppu8Plane[1] = cast(addressof(inputImg.ppu8Plane[0].contents) + (inputImg.pi32Pitch[0] * inputImg.i32Height), c_ubyte_p)
        inputImg.ppu8Plane[2] = cast(0, c_ubyte_p)
        inputImg.ppu8Plane[3] = cast(0, c_ubyte_p)
    elif ASVL_COLOR_FORMAT.ASVL_PAF_NV21 == inputImg.u32PixelArrayFormat:
        inputImg.ppu8Plane[0] = cast(imagedata, c_ubyte_p)
        inputImg.ppu8Plane[1] = cast(addressof(inputImg.ppu8Plane[0].contents) + (inputImg.pi32Pitch[0] * inputImg.i32Height), c_ubyte_p)
        inputImg.ppu8Plane[2] = cast(0, c_ubyte_p)
        inputImg.ppu8Plane[3] = cast(0, c_ubyte_p)
    elif ASVL_COLOR_FORMAT.ASVL_PAF_YUYV == inputImg.u32PixelArrayFormat:
        inputImg.ppu8Plane[0] = cast(imagedata, c_ubyte_p)
        inputImg.ppu8Plane[1] = cast(0, c_ubyte_p)
        inputImg.ppu8Plane[2] = cast(0, c_ubyte_p)
        inputImg.ppu8Plane[3] = cast(0, c_ubyte_p)
    else:
        print(u'unsupported yuv format')
        exit(0)

    inputImg.gc_ppu8Plane0 = imagedata
    return inputImg

def loadImage(filePath):
    """
    加载图片
    """
    bufferInfo = ImageLoader.getI420FromFile(filePath)
    inputImg = ASVLOFFSCREEN()
    inputImg.u32PixelArrayFormat = ASVL_COLOR_FORMAT.ASVL_PAF_I420
    inputImg.i32Width = bufferInfo.width
    inputImg.i32Height = bufferInfo.height
    inputImg.pi32Pitch[0] = inputImg.i32Width
    inputImg.pi32Pitch[1] = inputImg.i32Width // 2
    inputImg.pi32Pitch[2] = inputImg.i32Width // 2
    inputImg.ppu8Plane[0] = cast(bufferInfo.buffer, c_ubyte_p)
    inputImg.ppu8Plane[1] = cast(addressof(inputImg.ppu8Plane[0].contents) + (inputImg.pi32Pitch[0] * inputImg.i32Height), c_ubyte_p)
    inputImg.ppu8Plane[2] = cast(addressof(inputImg.ppu8Plane[1].contents) + (inputImg.pi32Pitch[1] * inputImg.i32Height // 2), c_ubyte_p)
    inputImg.ppu8Plane[3] = cast(0, c_ubyte_p)

    inputImg.gc_ppu8Plane0 = bufferInfo.buffer

    return inputImg

