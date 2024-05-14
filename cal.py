import math
''' predict == ouput , label == real value
 only support one dimension dataset
 The functions have been vaildated with sklearn metric'''
# pearson相关系数
def cal_R(predict, label):
    m_mean = 0
    p_mean = 0
    for i in range(0, label.shape[0]):
        m_mean = m_mean + label[i]
        p_mean = p_mean + predict[i]

    m_mean = m_mean / label.shape[0]
    p_mean = p_mean / label.shape[0]

    ra = 0  # 相关系数分子
    rb = 0  # 相关系数分母1
    rc = 0  # 相关系数分母2
    R = 0
    for i in range(0, label.shape[0]):
        ra = ra + (predict[i] - p_mean) * (label[i] - m_mean)
        rb = rb + (predict[i] - p_mean) ** 2
        rc = rc + (label[i] - m_mean) ** 2
    R = ra / math.sqrt(rb * rc)

    return R

def cal_MAE(predict, label):
    mae_loss = 0
    for i in range(0, label.shape[0]):
        mae_loss = mae_loss + abs(predict[i] - label[i])

    mae_loss = mae_loss / label.shape[0]

    return mae_loss

def cal_RMSE(predict, label):
    mse_loss = 0
    for i in range(0, label.shape[0]):
        mse_loss = mse_loss + (predict[i] - label[i]) ** 2
    mse_loss = mse_loss / label.shape[0]
    rmse_loss = math.sqrt(mse_loss)

    return rmse_loss

def cal_MAPE(predict, label):
    mape = 0
    for i in range(0, label.shape[0]):
        mape = mape + abs((predict[i] - label[i]) / label[i])
    mape = mape / label.shape[0]

    return  mape

# 不是相关系数的直接平方
def cal_R2(predict, label):
    m_mean = 0
    p_mean = 0
    for i in range(0, label.shape[0]):
        m_mean = m_mean + label[i]
        p_mean = p_mean + predict[i]

    m_mean = m_mean / label.shape[0]
    p_mean = p_mean / label.shape[0]

    ra = 0  # 相关系数分子
    rb = 0  # 相关系数分母1
    # rc = 0  # 相关系数分母2
    R = 0
    for i in range(0, label.shape[0]):
        ra = ra + (predict[i] - label[i]) ** 2
        rb = rb + (label[i] - m_mean) ** 2
    R2 = 1 - ra / rb
    return R2