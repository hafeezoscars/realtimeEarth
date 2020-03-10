
#!/usr/bin/env python 
# -*- coding: utf-8 -*-

STATEMENT = """
	realtimeEarth.py
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	从日本的地球同步卫星向日葵8号(Himawari 8 (ひまわり8号))获取实时高清地球图像，并且设置为桌面地址

	关于向日葵8号卫星
	官网:http://himawari8.nict.go.jp/
	维基百科：https://en.wikipedia.org/wiki/Himawari_8
	向日葵8号搭载 H-IIA202火箭在日本时间 2014年10月7日14时16分00秒 于 种子岛宇宙中心 发射升空[6]，
	其后14时43分57秒卫星与火箭成功分离[7]，同月16日19时00分确认其进入静止轨道
	
	目的：其作用为提供日本、东亚及西太平洋之周边的天气预报、台风、暴雨、气候变化的观察、预测等相关之报告，
	同时负责确保船只与航空的安全以及观察地球之环境

	制造厂商	三菱电机
	卫星平台	DS2000
	姿态控制	3轴姿态控制
	寿星		卫星：15年
				观察仪器：8年
	卫星重量	发射时：3.5t
				进入轨道后：1.3t
	观察传感器	AHI (Advanced Himawari Imager) 16频段 宇宙环境观察 (SEDA)
	观察频度	全球观察：10分钟/1次
				日本附近：2.5分钟/1次
	静止经纬度	赤道，东经140.7°附近
	图像传送	使用商用通信卫星传送
--------------------------------------------------------------------------
	CODE BY HAFEEZ（2020/3/8  为了新型冠状病毒2019-nCoV疫情爆发后的NASA航天梦）
"""


import os
import datetime
import requests
import win32con
import time
from PIL import Image
from PIL import ImageChops
from win32 import win32api, win32gui


def compareImgs(path_one, path_two):

	image_one = Image.open(path_one)
	image_two = Image.open(path_two)
	
	diff = ImageChops.difference(image_one, image_two)
	if diff.getbbox() is None:
		print("由于网络原因下载的图片文件损坏")
		print("正在等待下一次更新...\n")
		time.sleep(30)
		# 图片与 NoImage.png 相同，返回失败
		return False
	else:
		print('图片文件内容正常')
		return True

    
def downloadImg(url, imgName, savePath):

	# print("img_url: %s \n正在下载图片 请稍等..." % url)
	print('正在下载图片 请稍等...')
	try:
		img = requests.get(url, timeout=10)
		with open(savePath, 'wb+') as imgfile:
			imgfile.write(img.content)
			print("图片下载成功")
			print("图片保存成功	"+ imgName)
	except:
		print("图片下载失败，请更换网络或稍后再试\n")
		return False
	return compareImgs(savePath, os.getcwd() + '/Img/NoImage.png')



def setDesktopBackground(imgfrompath):
	try:
		key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,'Control Panel\\Desktop',0,win32con.KEY_SET_VALUE)
		win32api.RegSetValueEx(key,'WallpaperStyle',0,win32con.REG_SZ,'0')
		win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,imgfrompath,1+2)
		print("壁纸设置成功\n")
	except:
		print("壁纸设置失败，请以管理员身份运行\n")


def imageData():
	# 获取格林威治格式化时间并且减去40分钟(最新的图片可能获取不到)		
	realtime_gm = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
	realtime_strf = realtime_gm.strftime("%Y/%m/%d/%H%M")

	# 时间分钟向下取整数
	realtime_list = list(realtime_strf)
	realtime_list[-1] = '0'	
	realtime_strf = "".join(realtime_list)

	img_name = realtime_strf.replace('/','_') + "00_0_0.png"
	img_path = os.getcwd() + '/Img'
	if not os.path.exists(img_path):
		os.mkdir(img_path)
	img_path = img_path + '/' + img_name

	return ("http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/" + realtime_strf + "00_0_0.png",img_name,img_path)

	
def main():
	print(STATEMENT)
	while True:
		url, name, path = imageData()
		while not downloadImg(url, name, path):
			url, name, path = imageData()
			pass
		setDesktopBackground(path)
		print("正在等待下一次(10分钟后)更新...")
		time.sleep(60*10)
		
	




if __name__ == '__main__':
	main()
