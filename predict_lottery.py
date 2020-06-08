import xml.etree.ElementTree as ET
import os
from xml.dom import minidom
import random
import datetime

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

def gen_distri(gen):
    i = 0
    j = 0
    k = 0
    for n in gen:
        if n > 0 and n < 12:
            i = i+1
        elif n > 11 and n < 23:
            j = j+1
        else:
            k = k+1    
    return i,j,k


def similarity(g1,g2):
    s = 0
    for x in g1:
        for y in g2:
            if y == x:
                s = s+1
    return s

def odd_even_count(g):
    s = 0
    for item in g:
        if item % 2 == 0:
            s = s+1
    return 6-s,s

def format_string(g):
    str1 = ''
    for index,item in enumerate(g):
        x1 = item // 10
        x2 = item % 10
        str1 = str1 + str(x1) + str(x2)
        if index+1 != len(g):
            str1 = str1 + ' '
        else:
            return str1

def next_date(s):
    date_split = s.split('/')
    dt = datetime.date(int(date_split[0]),int(date_split[1]),int(date_split[2]))
    week_day = dt.weekday()+1
    if week_day == 4:
        st = datetime.datetime.strptime(s, '%Y/%m/%d') + datetime.timedelta(days=3)
        return st.strftime('%Y/%m/%d')
    else:
        st = datetime.datetime.strptime(s, '%Y/%m/%d') + datetime.timedelta(days=2)
        return st.strftime('%Y/%m/%d')

def gen_red_in_sequence(value_length):
    red_balls = []
    red_pool = [x+1 for x in range(value_length)]
    #generate first ball
    red_first = random.sample(red_pool,1)
    red_pool.remove(red_first[0])
    red_balls.append(red_first[0])

    #generate second ball
    red_second = random.sample(red_pool,1)
    red_pool.remove(red_second[0])
    red_balls.append(red_second[0])

    red_third = random.sample(red_pool,1)
    red_pool.remove(red_third[0])
    red_balls.append(red_third[0])

    red_fourth = random.sample(red_pool,1)
    red_pool.remove(red_fourth[0])
    red_balls.append(red_fourth[0])

    red_fifth = random.sample(red_pool,1)
    red_pool.remove(red_fifth[0])
    red_balls.append(red_fifth[0])

    red_sixth = random.sample(red_pool,1)
    red_pool.remove(red_sixth[0])
    red_balls.append(red_sixth[0])

    return red_balls
def number_gener_sta(simi_check = 0.25, distri_same = 0.05, bl_red = 0.20 , bl_bl = 0.10):
    with open(r'E:\Code\file\record_lottery.xml','r') as xml_file:
        tree = ET.parse(xml_file)
    root = tree.getroot()
    index_string = root.find('index').text
    index = int(root.find('index').text)
    index_key = ".//item[@number=\'{0}\']".format(index_string)
    index_ele = root.find(index_key)
    index_term = int(index_ele.find('term').text)
    index_date = index_ele.find('date').text

    red_neighbor_string = index_ele.find('red').text.split()
    red_neighbor = []

    for item in red_neighbor_string:
        red_neighbor.append(int(item))


    blue_neighbor = int(index_ele.find('blue').text)
    #random.sample(1+range(33), 10)
    indent(root)
    tree.write(r'E:\Code\file\record_lottery.xml',encoding="utf-8", xml_declaration=True)

    red_group = []
    blue = 0
    #generate red number group
    while True:
        g1 = gen_red_in_sequence(33)
        s1 = similarity(g1,red_neighbor)
        #red neighbor similarity check
        if s1 == 2:
            if random.uniform(0,1) > simi_check:
                continue
        elif s1 > 2:
            continue
        rnd = gen_distri(red_neighbor)
        gd = gen_distri(g1)
        #distribution check
        if gd == rnd:
            if random.uniform(0,1) > distri_same:
                continue
        if (5 in gd) or (6 in gd):
            continue
        #parity check
        oe = odd_even_count(g1)
        if 0 in oe:
            continue
        red_group = g1
        break

    #generate blue number 
    while True:
        g2 = random.sample([x+1 for x in range(16)], 1)
        g3 = g2[0]
        if g3 in red_group:
            if random.uniform(0,1) > bl_red:
                continue
        if g3 == blue_neighbor:
            if random.uniform(0,1) > bl_bl:
                continue
        blue = g2
        break

    red_group.sort()

    red_group_string = format_string(red_group)

    blue_string = format_string(blue)
    return [index,index_term,index_date,red_group_string,blue_string]

#generate output and record it in record_gen.xml
record_gen = []
lucky_number_red = '01 04 16 21 24 32'
lucky_number_blue = '08'

for i in range(2):
    out1 = number_gener_sta()
    record_gen.append(out1)

with open(r'E:\Code\file\record_gen.xml','r') as xml_file:
    tree = ET.parse(xml_file)
root = tree.getroot()
index_string_gen = root.find('index').text
index = record_gen[0][0]
if  (index+1) > int(index_string_gen):
    root.find('index').text = str(index+1)
    elem = ET.Element('item')
    elem.set('number',str(index+1))

    index_term = record_gen[0][1]
    index_next_date = next_date(record_gen[0][2])
    year_next = index_next_date.split('/')[0]
    year_cur = record_gen[0][2].split('/')[0]
    
    elem_term = ET.Element('term')
    if year_next != year_cur:
        elem_term.text = "1"
    else:
        elem_term.text = str(index_term+1)
    elem.append(elem_term)

    
    elem_next_date = ET.Element('date')
    elem_next_date.text = index_next_date
    elem.append(elem_next_date)
    #lucky element
    elem_lucky = ET.Element('lucky')     
    elem_red = ET.Element('red')
    elem_red.text = lucky_number_red
    elem_lucky.append(elem_red)

    elem_blue = ET.Element('blue')
    elem_blue.text = lucky_number_blue
    elem_lucky.append(elem_blue)

    elem_prize = ET.Element('prize')
    elem_prize.text = 'empty'
    elem_lucky.append(elem_prize)

    elem.append(elem_lucky)
    #sta element
    elem_sta = ET.Element('sta')     
    elem_red = ET.Element('red')
    elem_red.text = record_gen[0][3]
    elem_sta.append(elem_red)

    elem_blue = ET.Element('blue')
    elem_blue.text = record_gen[0][4]
    elem_sta.append(elem_blue)

    elem_prize = ET.Element('prize')
    elem_prize.text = 'empty'
    elem_sta.append(elem_prize)

    elem.append(elem_sta)

    #observe element
    elem_obs = ET.Element('obs')     
    elem_red = ET.Element('red')
    elem_red.text = record_gen[1][3]
    elem_obs.append(elem_red)

    elem_blue = ET.Element('blue')
    elem_blue.text = record_gen[1][4]
    elem_obs.append(elem_blue)

    elem_prize = ET.Element('prize')
    elem_prize.text = 'empty'
    elem_obs.append(elem_prize)

    elem.append(elem_obs)

    root.append(elem)

indent(root)
tree.write(r'E:\Code\file\record_gen.xml',encoding="utf-8", xml_declaration=True)








