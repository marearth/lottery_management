import xml.etree.ElementTree as ET
import os
from xml.dom import minidom

def similarity(g1,g2):
    s = 0
    for x in g1:
        for y in g2:
            if y == x:
                s = s+1
    return s
def prize_result(red_truth,red_pre,blue_shot):
    sim_red = similarity(red_truth,red_pre)
    if sim_red == 6:
        if blue_shot:
            return 'first(at most 10,000,000 yuan)'
        else:
            return 'second(at most 5,000,000 yuan'
    elif sim_red == 5:
        if blue_shot:
            return 'third(3000 yuan)'
        else:
            return 'fourth(200 yuan)'
    elif sim_red == 4:
        if blue_shot:
            return 'fourth(200 yuan)'
        else:
            return 'fifth(10 yuan)'
    elif sim_red == 3:
        if blue_shot:
            return 'fifth(5 yuan)'
        else:
            return 'nothing'
    else:
        if blue_shot:
            return 'sixth(5 yuan)'
        else:
            return 'nothing'

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

with open(r'E:\Code\file\record_gen.xml','r') as xml_file:
    tree = ET.parse(xml_file)
root = tree.getroot()
index_string_gen = root.find('index').text
index_key = ".//item[@number=\'{0}\']".format(index_string_gen)

with open(r'E:\Code\file\record_lottery.xml','r') as xml_file:
    tree_lot = ET.parse(xml_file)
root_lot = tree_lot.getroot()

index_ele_lot = root_lot.find(index_key)
index_ele = root.find(index_key)
lucky_prize = index_ele.find('lucky').find('prize').text

if not (index_ele_lot is None) and (lucky_prize == 'empty'):
    red_string_truth = index_ele_lot.find('red').text
    blue_string_truth = index_ele_lot.find('blue').text
    red_truth = []
    for item in red_string_truth.split():
        red_truth.append(int(item))
    #evaluate lucky prediction
    red_string_pre_lucky = index_ele.find('lucky').find('red').text
    blue_string_pre_lucky = index_ele.find('lucky').find('blue').text
    red_pre_lucky = []
    for item in red_string_pre_lucky.split():
        red_pre_lucky.append(int(item))
    blue_shot_lucky = (blue_string_truth == blue_string_pre_lucky)
    result_lucky = prize_result(red_truth,red_pre_lucky,blue_shot_lucky)
    index_ele.find('lucky').find('prize').text = result_lucky
    #evaluate statistical prediction
    red_string_pre_sta = index_ele.find('sta').find('red').text
    blue_string_pre_sta = index_ele.find('sta').find('blue').text
    red_pre_sta = []
    for item in red_string_pre_sta.split():
        red_pre_sta.append(int(item))
    blue_shot_sta = (blue_string_truth == blue_string_pre_sta)
    result_sta = prize_result(red_truth,red_pre_sta,blue_shot_sta)
    index_ele.find('sta').find('prize').text = result_sta
    #evaluate observe prediction
    red_string_pre_obs = index_ele.find('obs').find('red').text
    blue_string_pre_obs = index_ele.find('obs').find('blue').text
    red_pre_obs = []
    for item in red_string_pre_obs.split():
        red_pre_obs.append(int(item))
    blue_shot_obs = (blue_string_truth == blue_string_pre_obs)
    result_obs = prize_result(red_truth,red_pre_obs,blue_shot_obs)
    index_ele.find('obs').find('prize').text = result_obs

indent(root)
tree.write(r'E:\Code\file\record_gen.xml',encoding="utf-8", xml_declaration=True)




    