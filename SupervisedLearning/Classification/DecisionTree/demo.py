import ID3 as id3
import TreePlot as tp

# dataSet,featureNames = id3.createDataSet()
# tempFeatureNames = featureNames[:]
# myTree = id3.createTree(dataSet, tempFeatureNames)
# id3.storeTree(myTree, './SupervisedLearning/Classification/DecisionTree/resultTree.txt')
# testTree = id3.grabTree('./SupervisedLearning/Classification/DecisionTree/resultTree.txt')
# print(id3.classify(testTree, featureNames, [1,1]))
# print(id3.classify(testTree, featureNames, [0,1]))

fr = open('./SupervisedLearning/Classification/DecisionTree/lenses.txt')
lenses = [line.strip().split('\t') for line in fr.readlines()]
featureNames = ['age', 'prescript', 'astigmatic', 'tearRate']
tempFeatureNames = featureNames[:]
lensesTree = id3.createTree(lenses, tempFeatureNames)
print(lenses)
print(lensesTree)
tp.createPlot(lensesTree)
