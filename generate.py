import os
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from deepforest import CascadeForestRegressor
from lightgbm import LGBMRegressor
import os
# 提取出来的同时，用数组的方式保存改位置索引，跑完代码后按索引放入nc文件，并制作新的掩码数组

root_path = "F:\\Global_CO2_Fusion_research\\"
generate_path = root_path + "generate\\"
LAI_path = root_path + "LAI\\"
era5_path = root_path + "era5\\"
LandScan_path = root_path + "LandScan\\"
EDGAR_path = root_path + "EDGAR\\"
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

model_file = root_path + "train\\checkpoint\\DF-LGB"

model = CascadeForestRegressor(use_predictor=True)
model.set_predictor(LGBMRegressor())
model.load(model_file)
for root, dirs, files in os.walk(generate_path):
    for file in files:
        lon = None
        lat = None
        name = file[-9:]
        print(name)
        OCO2_file = Dataset(generate_path + file, "r+")
        XCO2 = OCO2_file.variables["XCO2"][:]
        XCO2 = np.ma.ravel(XCO2)
        # print(len(XCO2.compressed()))


        if lon == None or lat == None:
            lon = np.zeros((1800, 3600))
            for k in range(0, 1800):
                lon[k] = np.array(OCO2_file.variables['lon'][:])
            lon = np.ravel(lon)

            lat = np.zeros((3600, 1800))
            for k in range(0, 3600):
                lat[k] = np.array(OCO2_file.variables['lat'][:])
            lat = lat.T
            lat = np.ravel(lat)


        LAI_file = Dataset(LAI_path + "LAI_" + name)
        LAI = LAI_file.variables["LAI"][:]
        LAI = np.ma.ravel(LAI)
        # print(len(LAI.compressed()))

        for index,path in enumerate(path_list):
            era_file = Dataset(path + era5_list[index] + "_" + name)
            globals()[era5_list[index]] = era_file.variables[era5_list[index]][:]
            globals()[era5_list[index]] = np.ma.ravel(globals()[era5_list[index]])
            # print(len(globals()[era5_list[index]].compressed()))

        EDGAR_file = Dataset(EDGAR_path + "emi_" + name[0:4] + ".nc")
        EDGAR = EDGAR_file.variables["emissions"][:]
        EDGAR = np.ma.ravel(EDGAR)
        # print(len(EDGAR.compressed()))

        LS_file = Dataset(LandScan_path + "LS_" + name[0:4] + ".nc")
        LS = LS_file.variables["population"][:]
        LS = np.ma.ravel(LS)
        # print(len(LS.compressed()))

        index_list = list()
        mask = XCO2.mask | LAI.mask | LS.mask
        XCO2.mask = mask
        print(len(XCO2.compressed()))
        for k in range(len(mask)):
            if mask[k] == False:
                index_list.append(k)
        print(len(index_list)) # 索引长度应为1574070

        dataset = list()
        for i, v in enumerate(index_list):
            XCO2_value = XCO2[v]
            lon_value = lon[v]
            lat_value = lat[v]
            year_value = int(name[0:4])
            month_value = int(name[4:6])
            LAI_value = LAI[v]
            d2m_value = d2m[v]
            t2m_value = t2m[v]
            sp_value = sp[v]
            tp_value = tp[v]
            u10_value = u10[v]
            v10_value = v10[v]
            EDGAR_value = EDGAR[v]
            LS_value = LS[v]
            sample = np.array([XCO2_value, lon_value, lat_value, year_value, month_value, LAI_value, d2m_value,
                               t2m_value, sp_value, tp_value, u10_value, v10_value, EDGAR_value, LS_value])
            dataset.append(sample)

        # 列表转为数组
        dataset = np.array(dataset)
        # 送入模型
        output = model.predict(dataset)

        for i, v in enumerate(index_list):
            XCO2.data[v] = output[i]
        XCO2 = XCO2.reshape(1800, 3600)
        OCO2_file.variables["XCO2"][:] = XCO2
        OCO2_file.variables['XCO2'].long_name = 'CO2'
        OCO2_file.renameVariable("XCO2", "CO2")
        OCO2_file.close()
        newfile = file[1:]
        os.rename(root + file, root + newfile)


