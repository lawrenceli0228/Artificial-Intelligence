import re
import sys
import numpy as np



class Dot_dtl():
    def __init__(self, lab=None, split_value=None, split_attr=None, left=None, right=None, hasChild=False):
        self.lab = lab
        self.split_value = split_value
        self.split_attr = split_attr
        self.left = left
        self.right = right
        self.hasChild = hasChild


def read_fi(infrom_fi):
    tr_file = open(infrom_fi[1])
    te_file = open(infrom_fi[2])
    m_ef = int(infrom_fi[3])
    return tr_file, te_file, m_ef


def delete_s(l1):
    l1 = re.sub(r"^\s+|\s+$", "", l1)
    co_Data = re.split('\s+', l1)
    return co_Data


def add_attr(attr, data):
    if len(attr) > 0:
        attr = float(attr)
        data.append(attr)
    return data


def add_dict(data_labels, data_a, r_da_ta):
    dict = {}
    for i in range(len(data_labels)):
        dict[data_labels[i]] = data_a[i]
    r_da_ta.append(dict)
    return r_da_ta


def de_data_set(data_set, tr_attr):
    switch = False
    r_da_ta = []
    da_et = []
    da_at = get_attr(tr_attr)
    for l1 in data_set:
        co_Data = delete_s(l1)
        if switch == True:
            data = []
            for attr in co_Data:
                data_a = add_attr(attr, data)
            if len(data_a) == len(da_at):
                da_et = add_dict(da_at, data_a, r_da_ta)
        else:
            switch = True
    if da_at[-1] == 'quality':
        label = da_at[-1]
        return label, da_et
    return da_at, da_et


def co_label(tr_set, la_bel):
    for i in range(len(tr_set) - 1):
        if not (tr_set[i][la_bel] == tr_set[i + 1][la_bel]):
            return False
    return True


def co_attr_val(tr_set, attr_val):
    for i in range(len(tr_set) - 1):
        for val in attr_val:
            if (tr_set[i][val] != tr_set[i + 1][val]):
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
        tr_set.sort(key=lambda trainSet: trainSet[la_bel])
        la = fre_val(tr_set, la_bel)
        dot = Dot_dtl(lab=la)
        return dot

    attr, splitVal = ch_split(tr_set, attr_val)

    dot = Dot_dtl(split_value=splitVal,split_attr=attr,hasChild=True)


    le_Su_Set, ri_Su_Set = split(tr_set, splitVal, attr)
    dot.left = decsion_t(attr_val, la_bel, le_Su_Set, min_ef)
    dot.right = decsion_t(attr_val, la_bel, ri_Su_Set, min_ef)
    return dot


def split(tr_set, splitVal, attr):
    le_Su_Set = []
    ri_Sub_Set = []
    for each_data in tr_set:
        if each_data[attr] <= splitVal:
            le_Su_Set.append(each_data)
        else:
            ri_Sub_Set.append(each_data)
    return le_Su_Set, ri_Sub_Set


def ch_split(trainSet, tr_attrs):
    fi_attr_en = ""
    fi_split_en = 0.0
    fi_gain_en = 0.0
    for each_attr in tr_attrs:
        trainSet.sort(key=lambda trainSet: trainSet[each_attr])
        for i in range(len(trainSet) - 1):
            split = 0.5 * (trainSet[i][each_attr] + trainSet[i + 1][each_attr])
            gain = inf_gain(trainSet, each_attr, split)
            if gain > fi_gain_en:
                fi_gain_en = gain
                fi_split_en = split
                fi_attr_en = each_attr

    return fi_attr_en, fi_split_en


def inf(dataset):
    #  dataset is part dataset not whole set
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

    final_result = ir - (l_G + g_G)
    return final_result


def pre_i_t(dot_tree, test_data):
    while dot_tree.hasChild:
        if test_data[dot_tree.split_attr] <= dot_tree.split_value:
            dot_tree = dot_tree.left
        else:
            dot_tree = dot_tree.right
    return dot_tree.lab


def get_attr(data_set):
    label = []
    switch = 0
    for each in data_set:
        temp = delete_s(each)
        if switch == 0:
            label = temp
            switch += 1
    return label


def m_l(re_fi):
    tr_attr = open(re_fi[1])
    te_attr = open(re_fi[2])
    tr_file, te_file, min_ef = read_fi(re_fi)
    la_bel, tr_set = de_data_set(tr_file, tr_attr)
    attr_val, test_data_Set = de_data_set(te_file, te_attr)
    return la_bel, attr_val, tr_set, test_data_Set, min_ef


re_fi = sys.argv
la_bel, attr_val, tr_set, test_data_Set, min_ef = m_l(re_fi)
dot_tree = decsion_t(attr_val, la_bel, tr_set, min_ef)

for tstdt in test_data_Set:
    print(pre_i_t(dot_tree, tstdt))





