import matplotlib.pyplot as plt

# 定义文本框和箭头格式
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")
# 用来正常显示中文
plt.rcParams['font.sans-serif']=['SimHei']

# 获取树的叶子节点数量
def getLeafNum(myTree):
    leafNum = 0
    firstKey = list(myTree)[0]
    secondDict = myTree[firstKey]
    for key in secondDict.keys():
        # 判断节点的数据类型是否为字典
        if type(secondDict[key]).__name__=='dict':
            leafNum += getLeafNum(secondDict[key])
        else:
            leafNum += 1
    return leafNum

# 获取树的高度
def getTreeDepth(myTree):
    depth = 0
    firstKey = list(myTree)[0]
    secondDict = myTree[firstKey]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = getTreeDepth(secondDict[key]) + 1
        else:
            thisDepth = 1
        if thisDepth > depth:
            depth = thisDepth
    return depth

# 绘制带箭头的注解
def plotNode(nodeText, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeText, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)
    
# 计算父子节点的中间位置，并添加简单的文本信息
def plotMidText(centerPt, parentPt, txtString):
    xMid = (parentPt[0]-centerPt[0])/2.0 + centerPt[0]
    yMid = (parentPt[1]-centerPt[1])/2.0 + centerPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)
    
# 绘制树
def plotTree(myTree, parentPt, nodeTxt):
    leafNum = getLeafNum(myTree) 
    depth = getTreeDepth(myTree)
    firstKey = list(myTree)[0]
    centerPt = (plotTree.xOff + (1.0 + float(leafNum))/2.0/plotTree.totalW, plotTree.yOff)
    plotMidText(centerPt, parentPt, nodeTxt)
    plotNode(firstKey, centerPt, parentPt, decisionNode)
    secondDict = myTree[firstKey]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], centerPt, str(key)) 
        else: 
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), centerPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), centerPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

# 创建新图形
def createPlot(myTree):
    fig = plt.figure(1, facecolor="white")
    fig.clf()
    # createPlot.ax1 = plt.subplot(111, frameon=False)
    # nodePlot('决策节点', (0.5, 0.1), (0.1, 0.5), decisionNode)
    # nodePlot('叶子节点', (0.8, 0.1), (0.3, 0.8), leafNode)
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getLeafNum(myTree)) # 存储树的宽度
    plotTree.totalD = float(getTreeDepth(myTree)) # 存储树的深度
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(myTree, (0.5, 1.0), '')
    plt.show()