from math import log
import operator

# 创建数据集
def createDataSet():
    dataSet = [
        [1,1,'yes'],
        [1,1,'yes'],
        [1,0,'no'],
        [0,1,'no'],
        [0,1,'no']
    ]
    featureNames = ['no surfacing', 'flippers']
    return dataSet,featureNames

# 划分数据集，dataSet为待划分的数据集，axis表示划分数据集的特征，value表示需要划分特征的值
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for vec in dataSet:
        if vec[axis] == value:
            reducedVec = vec[:axis]
            reducedVec.extend(vec[axis+1:])
            retDataSet.append(reducedVec)
    return retDataSet

# 计算给定数据集的香农熵，熵越高则混合的数据也越多
def calcShannonEnt(dataSet):
    dataSetLen = len(dataSet)
    labels = {}
    # 为所有可能的分类创建字典
    for vec in dataSet:
        currentLabel = vec[-1]
        if currentLabel not in labels.keys():
            labels[currentLabel] = 0
        labels[currentLabel] += 1
    shannonEnt = 0.0
    for key in labels:
        # 计算所有类别发生的概率
        prob = float(labels[key])/dataSetLen
        # 以2为底求对数，计算香农熵
        shannonEnt -= prob * log(prob, 2) 
    return shannonEnt

# 遍历整个数据集，选取特征，划分数据集，计算信息增益，选出最好划分数据集的特征
def chooseBestFeatureToSplit(dataSet):
    featureNums = len(dataSet[0]) - 1 # 特征的数量
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0 # 最优信息增益
    bestFeature = -1 # 最好特征
    for i in range(featureNums):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = float(len(subDataSet))/len(dataSet)
            # 计算每种划分方式的信息熵
            newEntropy += prob * calcShannonEnt(subDataSet)
        # 计算最好的信息增益
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature
    
# 计算各个分类的出现次数，并返回次数最多的分类
def majorityLabel(labelList):
    labels = {}
    for label in labelList:
        if label not in labels.keys():
            labels[label] = 0
        labels[label] += 1
    sortedLabels = sorted(labels.items(), key = operator.itemgetter(1), reverse=True)
    return sortedLabels[0][0]


# 创建决策树
def createTree(dataSet, featureNames):
    labelList = [example[-1] for example in dataSet]
    # 类别完全相同则停止继续划分
    if labelList.count(labelList[0]) == len(labelList):
        return labelList[0]
    # 遍历完所有特征时返回出现次数最多的类别
    if len(dataSet[0]) == 1:
        return majorityLabel(labelList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatName = featureNames[bestFeat]
    myTree = {bestFeatName : {}}
    del(featureNames[bestFeat])
    bestFeatureVals = [example[bestFeat] for example in dataSet]
    uniqueVals = set(bestFeatureVals)
    for value in uniqueVals:
        subFeatNames = featureNames[:]
        myTree[bestFeatName][value] = createTree(splitDataSet(dataSet, bestFeat, value), subFeatNames)
    return myTree

# 序列化对象并保存为文件
def storeTree(inputTree, fileName):
    import pickle
    fw = open(fileName, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()

# 读取文件中存储的树
def grabTree(fileName):
    import pickle
    fr = open(fileName, 'rb')
    return pickle.load(fr)

# 使用决策树执行分类
def classify(inputTree, featureNames, testVec):
    firstKey = list(inputTree)[0]
    secondDict = inputTree[firstKey]
    featIndex = featureNames.index(firstKey)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                label = classify(secondDict[key], featureNames, testVec)
            else:
                label = secondDict[key]
    return label