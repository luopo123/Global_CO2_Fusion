## python 3.7
import os
import sklearn.ensemble
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score, KFold
from deepforest import CascadeForestRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
import numpy as np
from evaluation import cal
import joblib
import matplotlib.pyplot as plt
import torch
from torch import nn

import warnings
warnings.filterwarnings('ignore')

model_path = 'checkpoint\\DF-LGB'
pointDataset = np.load("..\\pointDataset.npy")
surfaceDataset = np.load("..\\surfaceDataset.npy")

# 直接训练
X_train, X_test, Y_train, Y_test = train_test_split(surfaceDataset, pointDataset, test_size=0.1)

model = CascadeForestRegressor(use_predictor=True)
# model = CascadeForestRegressor(n_estimators=2, n_trees=100, max_depth=8, min_samples_split=2,
#                                min_samples_leaf=1, use_predictor=True, predictor="forest", backend="sklearn")
model.set_predictor(LGBMRegressor())
# model.load(model_path)
model.fit(X_train, Y_train)


# feature_importances = model.get_layer_feature_importances(0)
# print(feature_importances)
'''==================train==================='''

Y_train_p = model.predict(X_train)

train_R2 = cal.cal_R2(Y_train_p, Y_train)
print('train R2:', train_R2)

train_MAE_loss = cal.cal_MAE(Y_train_p, Y_train)
print('train MAE:', train_MAE_loss)

train_RMSE_loss = cal.cal_RMSE(Y_train_p, Y_train)
print('train RMSE:', train_RMSE_loss)

train_MAPE = cal.cal_MAPE(Y_train_p,Y_train)
print('train MAPE:', train_MAPE)

'''===================test===================='''

predict = model.predict(X_test)

test_R2 = cal.cal_R2(predict, Y_test)
print('test R2:', test_R2)

test_MAE_loss = cal.cal_MAE(predict, Y_test)
print('test MAE:', test_MAE_loss)

test_RMSE_loss = cal.cal_RMSE(predict, Y_test)
print('test RMSE:', test_RMSE_loss)

test_MAPE = cal.cal_MAPE(predict, Y_test)
print('test MAPE:', test_MAPE)

if test_R2 > 0.92:
    model.save(model_path)

# # 10折交叉验证
# X = surfaceDataset
# Y = pointDataset
# R2s = list()
# MAEs = list()
# RMSEs = list()
#
# kfold = KFold(n_splits=10, shuffle=True)
#
# for train_index, test_index in kfold.split(X, Y):
#     X_train, X_test = X[train_index], X[test_index]
#     Y_train, Y_test = Y[train_index], Y[test_index]
#     model = LGBMRegressor()
#     # model = CascadeForestRegressor(use_predictor=True)
#     # model.set_predictor(RandomForestRegressor())
#     # model.set_predictor(LGBMRegressor())
#     # model.set_predictor(ExtraTreesRegressor())
#     model.fit(X_train, Y_train)
#
#     predict = model.predict(X_test)
#
#     R2s.append(cal.cal_R2(predict, Y_test))
#     MAEs.append(cal.cal_MAE(predict, Y_test))
#     RMSEs.append(cal.cal_RMSE(predict, Y_test))
#     del model
#
# for k in range(len(R2s)):
#     print("Fold {} R2: {:.4f}".format(k + 1, R2s[k]))
# R2s = np.array(R2s)
# print("     Average R2: {:.4f}".format(R2s.mean()))
#
# for k in range(len(MAEs)):
#     print("Fold {} MAE: {:.4f}".format(k + 1, MAEs[k]))
# MAEs = np.array(MAEs)
# print("     Average MAE: {:.4f}".format(MAEs.mean()))
#
# for k in range(len(RMSEs)):
#     print("Fold {} RMSE: {:.4f}".format(k + 1, RMSEs[k]))
# RMSEs = np.array(RMSEs)
# print("     Average RMSE: {:.4f}".format(RMSEs.mean()))
