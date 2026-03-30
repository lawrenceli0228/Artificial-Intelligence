import re
import sys
import numpy as np


class Dot_dtl():
    def __init__(self, dot_sp_atr=None, split_value=0, label=None):
        self.lab = label
        self.split_value = split_value
        self.split_attr = dot_sp_atr
        self.left = None
        self.right = None



def read_fi(infrom_fi):
    tr_file = open(infrom_fi[1])

    te_file = open(infrom_fi[2])

    m_ef = int(infrom_fi[3])

    return tr_file, te_file, m_ef

def delete_s(l1):
    l1 = l1.strip()
    co_Data = re.split('\s+', l1)
    return co_Data


def add_attr(attr,data):
    if len(attr) > 0:
        attr = float(attr)
        data.append(attr)
    return data

def add_dict(data_labels,data_a,r_da_ta):
    dict = {}
    for i in range(len(data_labels)):
        dict[data_labels[i]] = data_a[i]
    r_da_ta.append(dict)
    return r_da_ta

def de_data_set(data_set):
    count = False
    r_da_ta = []
    dataSet = []
    for l1 in data_set:
        co_Data =delete_s(l1)
        if count == True:
            data = []
            for attr in co_Data:
                data_a = add_attr(attr,data)
            if len(data_a) == len(data_labels):
                dataSet = add_dict(data_labels,data_a,r_da_ta)
        else:
            data_labels = co_Data
            count = True
    return data_labels, dataSet

def co_label(tr_set, la_bel):
    for i in range(len(tr_set) - 1):
        if not (tr_set[i][la_bel] == tr_set[i + 1][la_bel]):
            return False
    return True


def co_attr_val(tr_set, attr_val):
    for i in range(len(tr_set) - 1):
        for val in attr_val:
            if(tr_set[i][val] != tr_set[i + 1][val]):
                return False
    return True

def fre_val(trainSet, label):
    if len(trainSet) == 1:
        res = 5
        return res
    label_list = []
    for data in trainSet:
        label_list.append(data[label])
    label_list.sort()
    newlabel = np.array(label_list)
    int_array = newlabel.astype(int)
    res1 = np.bincount(int_array).argmax()

    return res1

def decsion_t(attr_val, la_bel, tr_set, min_ef):
    if len(tr_set) < min_ef or co_label(tr_set, la_bel) or co_attr_val(tr_set, attr_val):
        print("almost complete tree", len(tr_set), "&", co_label(tr_set, la_bel), "&", co_attr_val(tr_set, attr_val))

        tr_set.sort(key=lambda trainSet:trainSet[la_bel])
        n = Dot_dtl(label=fre_val(tr_set, la_bel))
        return n

    attr, splitVal = ch_split(tr_set, attr_val)
    #print("choose attribute ", attr_val.index(attr), "choose split value: ", splitVal)

    n = Dot_dtl(dot_sp_atr=attr, split_value=splitVal)

    le_Su_Set,ri_Su_Set = split(tr_set, splitVal,attr)
    n.left = decsion_t(attr_val, la_bel, le_Su_Set, min_ef)
    n.right = decsion_t(attr_val, la_bel, ri_Su_Set, min_ef)
    return n

def split(tr_set,splitVal,attr):
    le_Su_Set = []
    ri_Sub_Set = []
    for each_data in tr_set:
        if each_data[attr] <= splitVal:
            le_Su_Set.append(each_data)
        else:
            ri_Sub_Set.append(each_data)
    return le_Su_Set,ri_Sub_Set

def ch_split(trainSet, tr_attrs):
    fi_attr_en = ""
    fi_split_en = 0.0
    fi_gain_en = 0.0
    for each_attr in tr_attrs:
        trainSet.sort(key=lambda trainSet: trainSet[each_attr])
        for i in range(len(trainSet)-1):
            split = 0.5 * (trainSet[i][each_attr] + trainSet[i+1][each_attr])
            gain = inf_gain(trainSet, each_attr, split)
            if gain > fi_gain_en:
                fi_gain_en = gain
                fi_split_en = split
                fi_attr_en = each_attr

            #print("gain: ", gain, "best gain", bst_gain)

    return fi_attr_en, fi_split_en

def inf(dataset):
    m = float(len(dataset))
    counta = 0.0
    countb = 0.0
    countc = 0.0
    totalre = []
    to_i = 0.0
    for dt in dataset:
        if dt["quality"] == 5:
            counta += 1.0
        elif dt["quality"] == 6:
            countb += 1.0
        else:
            countc += 1.0
    totalre.append(counta)
    totalre.append(countb)
    totalre.append(countc)

    for i in totalre:
        if i > 0.0:
            p = i / m
            to_i -= p * np.log2(p)
    return to_i



def inf_gain(dataset, attr, split):
    ir = inf(dataset)
    s_part = []
    g_part = []

    for i in range(len(dataset)):
        if dataset[i][attr] <= split:
            s_part.append(dataset[i])
        else:
            g_part.append(dataset[i])


    s_pobi = len(s_part) / len(dataset)
    g_pobi = len(g_part) / len(dataset)
    l_G = s_pobi * inf(s_part)
    g_G = g_pobi * inf(g_part)

    return ir - l_G - g_G



re_fi = sys.argv
tr_file, te_file, min_ef = read_fi(re_fi)


attr_label_Set,  tr_set = de_data_set(tr_file)
la_bel = attr_label_Set[-1]

attr_val, test_data_Set = de_data_set(te_file)

dot_tree = decsion_t(attr_val, la_bel, tr_set, min_ef)


def predict(dot_tree=None, test_data=None):
    while dot_tree.lab == None:
        print("test_data[node.split_attr]: ", test_data[dot_tree.split_attr], "attribute : ", dot_tree.split_attr)
        if test_data[dot_tree.split_attr] <= dot_tree.split_value:

            dot_tree = dot_tree.left
        else:
            dot_tree = dot_tree.right
    return dot_tree.lab

for tstdt in test_data_Set:
    print(predict(dot_tree, tstdt))


'''
              dict = {}
                              for i in range(len(data_labels)):
                  dict[data_labels[i]] = data_a[i]
              r_da_ta.append(dict)
              
             for each_data in tr_set:
        if each_data[attr] <= splitVal:
            le_Su_Set.append(each_data)
        else:
            ri_Sub_Set.append(each_data)
              
              
'''
# print_tree(node)


'''
---------------------------- trainSet ---------------------------------------------------------------------------------------
trainSet sort by attribute:f_acid  {'f_acid': 5.7, 'v_acid': 0.26, 'c_acid': 0.25, 'res_sugar': 10.4, 'chlorides': 0.02, 
'fs_dioxide': 7.0, 'ts_dioxide': 57.0, 'density': 0.994, 'pH': 3.39, 'sulphates': 0.37, 'alcohol': 10.6, 'quality': 5.0} index:  0


trainSet sort by attribute:  {'f_acid': 8.6, 'v_acid': 0.23, 'c_acid': 0.46, 'res_sugar': 1.0, 'chlorides': 0.054, 
'fs_dioxide': 9.0, 'ts_dioxide': 72.0, 'density': 0.9941, 'pH': 2.95, 'sulphates': 0.49, 'alcohol': 9.1, 'quality': 6.0} index:  98
-------------------------------------------------------------------------------------------------------------------------------

-----------------------------label------------------------------------------------------------------------------------------
quality 5,6,7
-------------------------------------------------------------------------------------------------------------------------------

#print("attr: ", attr,"split value: ",split)
#print("node.split_value: ", node.split_value)
 #print("test_data[node.split_attr]: ", node.split_value)
#print("node.split_value: ", node.split_value)
 #print("node.label: ", node.label)
 #print("node.split_value: ", node.split_value)

#print()
#print("test label output: ")


   lessGain = np.array(smallpart)
    greatGain = np.array(greatpart)
    #information(smallpart)
    #information(greatpart)
    # print(psmallpart,pgreatpart)

    #print(lessG)
    #print("greatG: ",greatG)
    #print("lessG: ", lessG)

def informatin_part(data):
    res, recount = np.unique(data[...,-1],return_counts= True)

    print(res,recount)
    total = 0.0
    for i in recount:
        total += i
    #print(total)
    totalI = 0.0
    for i in recount:
        p = i / total
        totalI -= p * np.log2(p)
    return totalI


def calculateIGain(trainSet, label,small_part, great_part):
    m = float(len(trainSet))
    trainSet.sort(key=lambda trainSet: trainSet[label])
    small_part.sort(key=lambda small_part: small_part[label])
    great_part.sort(key=lambda great_part: great_part[label])

    for a in small_part:
        print("small_part ----- sort by label", a)

    count = 1.0
    inforCurrent = 0.0
    inforSmall = 0.0
    inforGreat = 0.0
    label_value = trainSet[0][label]
    for dt in trainSet:
        if dt[label] != label_value:
            probablity = count/m
            inforCurrent += 0 - probablity * np.log2(probablity)
            count = 1.0
        else:
            count += 1.0
    inforCurrent += 0 - probablity * np.log2(probablity)
    count = 1.0
    probablityOfLess = float(len(small_part)) / m
    probablityOfGreat = float(len(great_part)) / m
    label_value = small_part[0][label]
    for smdt in small_part:
        if smdt[label] != label_value:
            probablity = count / m
            inforSmall += 0 - probablity * np.log2(probablity)
            count = 1.0
        else:
            count += 1.0
    inforSmall += 0 - probablity * np.log2(probablity)
    count = 1.0
    for gtdt in great_part:
        if gtdt[label] != label_value:
            probablity = count / m
            inforGreat += 0 - probablity * np.log2(probablity)
            count = 1.0
    inforGreat += 0 - probablity * np.log2(probablity)
    return inforCurrent - (probablityOfLess * inforSmall + probablityOfGreat * inforGreat)


    print(len(train_data_set) - 1)
a = 0
for j in train_data_set:
    print("line: ", a, "-----", j)
    a = a + 1
i = 0
a = [1,2,3,4,5,6,7,8,9,10,11,124144,1,24,24,12]
while i < len(a) - 1:
    smallpart = a[:i + 1]
    greatpart = a[i + 1:]
    print(smallpart, "----", greatpart)
    i = i +1



                if trainSet[i+1][attribute] <= 0.5 *(trainSet[i][attribute] + trainSet[i+1][attribute]):
                i += 1
                continue
            smallpart = trainSet[:i+1]
            greatpart = trainSet[i+1:]


  index = 0
     for set in trainSet:
         print("--------------------------> trainSet sort by attribute: ", set, "index: ", index)
         index = index + 1

          for i in range(len(label_list)-1):
        if (label_list[i] == label_list[i+1]):
            count += 1
        else:
            if count > maxCount:
                res = label_list[i]
                maxCount = count
            elif count == maxCount:
                res = 'unknown' + str(res)
            count = 0
    if count > maxCount:
        res = label_list[i]
    elif count == maxCount:
        res = 'unknown' + str(res)
    print("res:", res)
'''