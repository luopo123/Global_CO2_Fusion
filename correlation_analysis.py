# python 2.7
# _*_coding:utf-8_*_
import math
from netCDF4 import Dataset
import os
import numpy as np
import arcpy
from arcpy.sa import *

root_path = "F:\\Global_CO2_Fusion_research\\"

NDVI_path = root_path + "NDVI_tif\\"

OCO2_path = root_path + "OCO2_result\\"
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
factor_list = ["XCO2", "LAI", "NDVI", "d2m", "t2m", "e", "sp", "tp", "u10", "v10"]
path_list = [OCO2_path, LAI_path, NDVI_path, d2m_path, t2m_path, e_path, sp_path, tp_path, u10_path, v10_path]
correlation_file = root_path + "correlation_analysis\\"
month = 201501
# 取数据
for k in range(0, 12):
    print month
    for i, v in enumerate(path_list):
        for root, dirs, files in os.walk(v):
            for file in files:
                if file.endswith(".nc"):
                    name = file[:-3]
                    if name[-6:] == str(month):
                        print name
                        # if name[0:4] == "XCO2" or name[0:3] == "LAI":
                        globals()[factor_list[i]] = arcpy.MakeNetCDFRasterLayer_md(in_netCDF_file=root + file,
                                                                                       variable=factor_list[i],
                                                                                       x_dimension="lon",
                                                                                       y_dimension="lat",
                                                                                       out_raster_layer=name,
                                                                                       band_dimension="",
                                                                                       dimension_values="",
                                                                                       value_selection_method="BY_VALUE",
                                                                                       cell_registration="CENTER")
                        # else:
                        #     globals()[factor_list[i]] = arcpy.MakeNetCDFRasterLayer_md(in_netCDF_file=root + file,
                        #                                              variable=factor_list[i],
                        #                                              x_dimension="longitude", y_dimension="latitude",
                        #                                              out_raster_layer=name,
                        #                                              band_dimension="", dimension_values="",
                        #                                              value_selection_method="BY_VALUE",
                        #                                              cell_registration="CENTER")
                # if file.endswith(".tif"):
                #     name = file[:-4]
                #     if name[-6:] == str(month):
                #
    BandCollectionStats([XCO2, LAI, NDVI_path + "NDVI_" + str(month) + ".tif", d2m, t2m, e, sp, tp, u10, v10],
                        correlation_file + str(month) + ".txt", "DETAILED")
    month = month + 1
arcpy.Delete_management("D:\\Users\\Documents\\ArcGIS\\Default.gdb")