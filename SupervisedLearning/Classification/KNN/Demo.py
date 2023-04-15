# 算法：
# （1）计算已知类别数据集中的点与当前点之间的距离
# （2）按照距离依次递增排序
# （3）选取与当前点距离最小的k个点
# （4）确定前k个点所在类别的出现频率
# （5）返回前k个点出现频率最高的类别作为当前点的预测分类

from numpy import *
import operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify(inputData, group, labels, k):
    dataSetSize = group.shape[0]
    # 计算距离
    diffMat = (tile(inputData, (dataSetSize,1)) - group) ** 2
    distances = (diffMat.sum(axis = 1)) ** 0.5
    # 排序
    sortDisIndicies = distances.argsort()
    # 选择距离最小的k个点
    selectPoints = {}
    for i in range(k):
        label = labels[sortDisIndicies[i]]
        # 计算前k个点所在类别的出现频率
        selectPoints[label] = selectPoints.get(label, 0) + 1
    # 排序，返回前k个点出现频率最高的类别
    sortSelectPoints = sorted(selectPoints.items(), key = operator.itemgetter(1), reverse = True)
    return sortSelectPoints[0][0]  

    

group, labels = createDataSet()
result = classify([1.0,1.0], group, labels, 3)
print(result)