import re
import sys
import numpy as np


class DTNode():
    def __init__(self, split_attr = None,split_value = 0, label = None ):
        self.label = label
        self.split_value = split_value
        self.split_attr = split_attr
        self.left = None
        self.right = None

def buildDataSet(file):
    num = 1
    return_data_set = []
    for line in file:
        line = line.strip()
        raw_data = re.split('\s+',line)
        if num > 1:
            data = []
            for val in raw_data:
                if len(val) > 0:
                    val = float(val)
                    data.append(val)
            if len(data) == len(data_labels):
                dict = {}
                for i in range(len(data_labels)):
                    dict[data_labels[i]] = data[i]
                return_data_set.append(dict)
        else:
            data_labels = raw_data
        num += 1
    return data_labels, return_data_set

def getConsistLabel(trainSet, label):
    i = 0
    while i < len(trainSet) - 1:
        if not (trainSet[i][label] == trainSet[i+1][label]):
            return False
        i += 1
    return True


def getConsistAttribute(trainSet, attributes):
    for i in range(len(trainSet) - 1):
        for attribute in attributes:
            if(trainSet[i][attribute] != trainSet[i+1][attribute]):
                return False
    return True



def confirmLabel(trainSet, label):
    if len(trainSet) == 1:
        return trainSet[0][label]

    label_list = []
    for data in trainSet:
        #print(data[label])
        label_list.append(data[label])
    label_list.sort()

    newlabel = np.array(label_list)
    int_array = newlabel.astype(int)
    res1 = np.bincount(int_array).argmax()

    return res1




def DTL(attributes, label, trainSet, minleaf):
    if len(trainSet) < minleaf or getConsistLabel(trainSet,label) or getConsistAttribute(trainSet, attributes):
        #print("almost complete tree", len(trainSet), "&", getConsistLabel(trainSet,label), "&", getConsistAttribute(trainSet, attributes))

        trainSet.sort(key=lambda trainSet:trainSet[label])
        n = DTNode(label=confirmLabel(trainSet, label))
        return n

    attr, splitVal = chooseSplit(trainSet, attributes)
    #print("choose attribute ", attributes.index(attr), "choose split value: ", splitVal)
    n = DTNode(split_attr=attr, split_value=splitVal)

    leftSubSet, rightSubSet = [], []
    for data in trainSet:
        if data[attr] <= splitVal:
            leftSubSet.append(data)
        else:
            rightSubSet.append(data)
    n.left = DTL(attributes, label, leftSubSet, minleaf)
    n.right = DTL(attributes, label, rightSubSet, minleaf)
    return n


def chooseSplit(trainSet, trainAttributes):
    bst_attr = ""
    bst_split = 0.0
    bst_gain = 0.0
    for attribute in trainAttributes:
        trainSet.sort(key=lambda trainSet: trainSet[attribute])

        for i in range(len(trainSet)-1):
            split = 0.5 * (trainSet[i][attribute] + trainSet[i+1][attribute])
            gain = informationGain(trainSet, attribute,split)
            if gain > bst_gain:
                bst_gain = gain
                bst_split = split
                bst_attr = attribute
                #print("choose attribute ", trainAttributes.index(bst_attr), "choose split value: ", bst_split)

            #print("gain: ", gain, "best gain", bst_gain)

    return bst_attr, bst_split




def information(dataset):
    m = float(len(dataset))
    counta = 0.0
    countb = 0.0
    countc = 0.0
    rescount = []
    totalI = 0.0
    for dt in dataset:
        if dt[label] == 5:
            counta += 1.0
        elif dt[label] == 6:
            countb += 1.0
        else:
            countc += 1.0
    rescount.append(counta)
    rescount.append(countb)
    rescount.append(countc)

    for i in rescount:
        if i > 0.0:
            p = i / m
            totalI -= p * np.log2(p)
    return totalI



def informationGain(dataset, attr, split):
    ir = information(dataset)
    print("ir", ir)
    smallpart = []
    greatpart = []

    for i in range(len(dataset)):
        if dataset[i][attr] <= split:
            smallpart.append(dataset[i])
        else:
            greatpart.append(dataset[i])


    psmallpart = len(smallpart) / len(dataset)
    pgreatpart = len(greatpart) / len(dataset)
    lessG = psmallpart * information(smallpart)
    greatG = pgreatpart * information(greatpart)

    result = ir - lessG - greatG
    print("gain",result)
    quit()
    return ir - lessG - greatG


args = sys.argv

train_file = open(args[1])

test_file = open(args[2])

minleaf = int(args[3])


attr_label_Set,  train_data_set = buildDataSet(train_file)
label = attr_label_Set[-1]


attrs, test_data_Set = buildDataSet(test_file)


node = DTL(attrs, label, train_data_set, minleaf)





def predict(node=None, test_data=None):
    while node.label == None:
        #print("test_data[node.split_attr]: ", test_data[node.split_attr], "attribute : ", node.split_attr)
        #print(node.split_value)
        if test_data[node.split_attr] <= node.split_value:

            node = node.left
            #predict(node,test_data)
        else:
            node = node.right
            #predict(node, test_data)
    return node.label

for tstdt in test_data_Set:
    print(predict(node, tstdt))