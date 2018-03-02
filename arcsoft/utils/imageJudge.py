#coding=utf-8

from pymediainfo import MediaInfo

media_info = MediaInfo.parse('../../lena.bmp')

print(media_info.tracks)
