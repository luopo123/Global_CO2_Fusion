# python 3.10
import math
from osgeo import gdal
from netCDF4 import Dataset
import os
import matplotlib.pyplot as plt
import numpy as np
import csv

root_path = "F:\\Global_CO2_Fusion_research\\"

NDVI_path = root_path + "NDVI_extract_tif_downscale\\"

OCO2_path = root_path + "OCO2_result\\"
LAI_path = root_path + "LAI\\"
era5_path = root_path + "era5\\"
LandScan_path = root_path + "LandScan\\"
EDGAR_path = root_path + "EDGAR\\"
ODIAC_path = root_path + "ODIAC\\"
gawPath = root_path + "monthly_csv_month\\"

d2m_path = era5_path + "d2m\\"
e_path = era5_path + "e\\"
sp_path = era5_path + "sp\\"
t2m_path = era5_path + "t2m\\"
tp_path = era5_path + "tp\\"
u10_path = era5_path + "u10\\"
v10_path = era5_path + "v10\\"
# e与LAI相关性过高，删除
era5_list = ["d2m", "t2m", "sp", "tp", "u10", "v10"]
path_list = [d2m_path, t2m_path, sp_path, tp_path, u10_path, v10_path]

# # input 数据组合
# surfaceData = list()
# for root, dirs, files in os.walk(OCO2_path):
#     for file in files:
#         name = file[5:11]
#         print(name)
#         OCO2File = Dataset(OCO2_path + file)
#         print(OCO2File.variables.keys())
#         print(len(OCO2File.variables['lat'][:]))  # 1800
#         print(len(OCO2File.variables['lon'][:]))  # 3600
#         # 将lon转成1800*3600的二维数组
#         lon = np.zeros((1800, 3600))
#         for k in range(0, 1800):
#             lon[k] = np.array(OCO2File.variables['lon'][:])
#         #将lat转成1800*3600的二维数组
#         lat = np.zeros((3600, 1800))
#         for k in range(0, 3600):
#             lat[k] = np.array(OCO2File.variables['lat'][:])
#         lat = lat.T
#         XCO2 = OCO2File.variables['XCO2'][:]
#         XCO2 = np.round(np.array(XCO2), 2)
#         #提取年月
#         year = np.full(1800 * 3600, int(file[5:9])).reshape(1800, 3600)
#         month = np.full(1800 * 3600, int(file[9:11])).reshape(1800, 3600)
#         # #提取NDVI
#         # NDVI_file = NDVI_path + "NDVI_" + name + ".tif"
#         # NDVI_data = gdal.Open(NDVI_file)
#         # im_width = NDVI_data.RasterXSize  # 栅格矩阵的列数
#         # im_height = NDVI_data.RasterYSize  # 栅格矩阵的行数
#         # NDVI = NDVI_data.ReadAsArray(0, 0, im_width, im_height)
#         # print(im_data.shape)  # (1737 * 3600)
#         # 提取LAI
#         LAI_file = Dataset(LAI_path + "LAI_" + name + ".nc")
#         LAI = LAI_file.variables['LAI'][:]
#         # 提取era5的数据
#         for n, item in enumerate(path_list):
#             era5_file = item + era5_list[n] + "_" + name + ".nc"  # 确定路径
#             era5_dataset = Dataset(era5_file) # 根据路径打开nc文件
#             globals()[era5_list[n]] = era5_dataset.variables[era5_list[n]][:] # 找到对应变量并用新变量记录
#         # EDGAR
#         EDGAR_file = Dataset(EDGAR_path + "emi_" + name[0:4] + ".nc")
#         EDGAR = EDGAR_file.variables['emissions'][:]
#         # # ODIAC
#         # ODIAC_file = Dataset(ODIAC_path + "emi_" + name + ".nc")
#         # ODIAC = ODIAC_file.variables['emissions'][:]
#         # LandScan
#         LandScan_file = Dataset(LandScan_path + "LS_" + name[0:4] + ".nc")
#         LandScan = LandScan_file.variables['population'][:]
#         dataset = np.array([XCO2, lon, lat, year, month, LAI, d2m, t2m, sp, tp, u10, v10, EDGAR, LandScan])  #  多余辅助因子这里还需要删除
#         surfaceData.append(dataset)
# surfaceData = np.array(surfaceData)
# print(surfaceData.shape)  # (84, 14, 1800, 3600)
# print(surfaceData.shape[0], surfaceData.shape[1], surfaceData.shape[2], surfaceData.shape[3])
# print(surfaceData[0, :, 0, 0])
# np.save("surfaceData", surfaceData)
#
# #处理站点数据，按月处理
# lat = list()
# lon = list()
# year = list()
# month = list()
# gawData = list()
# for root, dirs, files in os.walk(gawPath):
#     for file in files:
#         print('gaw'+file)
#         # single_lat = list()
#         # single_lon = list()
#         # single_gaw = list()
#         # single_time = list()
#         with open(gawPath+file) as f:
#             gawFile = csv.reader(f)
#             next(gawFile)
#             for row in gawFile:
#                 lat.append(float(row[1]))
#                 lon.append(float(row[2]))
#                 year.append(int(file[0:4]))
#                 month.append(int(file[4:6]))
#                 gawData.append(float(row[3]))
# print(lat)
# print(lon)
# print(year)
# print(month)
# print(gawData)
# data = [gawData, lon, lat, year, month]
# pointData = np.array(data)
# np.save("pointData", pointData)
#
#载入数据
#读取4维数据，并提取某个时间点某个位置的值和经纬度
surfaceData = np.load("surfaceData.npy")
print(surfaceData.shape[0], surfaceData.shape[1], surfaceData.shape[2], surfaceData.shape[3])
# print(surfaceData[1, :, 2, 2])
# [           -inf -1.79750000e+02  8.97500000e+01  2.01500000e+03
#   2.00000000e+00 -3.40282347e+38 -3.40282347e+38 -3.40282347e+38
#  -3.40282347e+38 -3.40282347e+38 -3.40282347e+38 -3.40282347e+38
#   2.14748365e+09]
# print(surfaceData[1, :, -1, -1])  #第一个索引是月份，第二个索引是经纬度值和值（确定某个面）（这里需要输入每个面的同一个位置的值），第三个和第四个是二维矩阵上的位置（行和列）
#  [           -inf  1.79950000e+02 -8.99500000e+01  2.01500000e+03
#   2.00000000e+00 -3.40282347e+38 -3.40282347e+38 -3.40282347e+38
#  -3.40282347e+38 -3.40282347e+38 -3.40282347e+38 -3.40282347e+38
#   2.14748365e+09]
pointData = np.load("pointData.npy")
print(pointData.shape[0], pointData.shape[1])
print(float(pointData[0, 0]))
#
#
# #
# #
#创建数据集
OCO2Dataset = list()
gawDataset = list()
for k in range(0, pointData.shape[1]):
        feature_value = float(pointData[0, k])
        feature_lon = float(pointData[1, k])
        feature_lat = float(pointData[2, k])
        feature_year = int(pointData[3, k])
        feature_month = int(pointData[4, k])
        index_lat = -int((feature_lat+90)*10+1)
        index_lon = int((feature_lon+180)*10)
        for i in range(0, surfaceData.shape[0]):
            if surfaceData[i, 3, index_lat, index_lon] == feature_year \
                and surfaceData[i, 4, index_lat, index_lon] == feature_month:
                if 0 < surfaceData[i, 0, index_lat, index_lon] \
                    and -100 <= surfaceData[i, 5, index_lat, index_lon] \
                    and -100 < surfaceData[i, 6, index_lat, index_lon] \
                    and -100 < surfaceData[i, 7, index_lat, index_lon] \
                    and -100 < surfaceData[i, 8, index_lat, index_lon] \
                    and -100 < surfaceData[i, 9, index_lat, index_lon] \
                    and -100 < surfaceData[i, 10, index_lat, index_lon] \
                    and -100 < surfaceData[i, 11, index_lat, index_lon] \
                    and -100 <= surfaceData[i, 12, index_lat, index_lon] \
                    and -100 <= surfaceData[i, 13, index_lat, index_lon] < 10000000:
                    # and abs(float(surfaceData[i, 0, index_lat, index_lon]) - feature_value) < 8\
                    gawDataset.append(feature_value)
                    OCO2Dataset.append(surfaceData[i, :, index_lat, index_lon]) #在面数据中找到点标签对应的点数据，时空匹配
                else:
                    print(pointData[:, k])
                    print(surfaceData[i, :, index_lat, index_lon])
gawDataset = np.array(gawDataset)
OCO2Dataset = np.array(OCO2Dataset)
np.save("surfaceDataset", OCO2Dataset)
np.save("pointDataset", gawDataset)


#读取数据测试
pointDataset = np.load("pointDataset.npy")
surfaceDataset = np.load("surfaceDataset.npy")
print(pointDataset.shape)  # 5423   5355
print(surfaceDataset.shape)
print(surfaceDataset[0], pointDataset[0])
print(surfaceDataset[1], pointDataset[1])
print(surfaceDataset[2], pointDataset[2])
# #
# #
