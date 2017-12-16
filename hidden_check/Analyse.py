# coding:utf-8
import json
import re
import threading
from .Node import Node

hidden_node = []
hidden_node_dict = {}


def start(outdomainnode):
    for node in outdomainnode:
        t = threading.Thread(target=check, args=(node,))
        t.start()
    for node in outdomainnode:
        t.join()
    return hidden_node


def check(node):
    '''
    :param node: 节点类，有多种css属性
    :return: hidden node
    '''
    while True:

        # 1 检测position，display,visibility {False，True}
        # boolean = node.is_displayed()
        # if boolean == False:
        #     hidden_node.append(node)
        #     hidden_node_dict[Node.get_url(node)] = '1'
        #     return False

        # 2 检测font-size 小于2即认为隐藏,写法为百分比，property得到的都为计算过后的大小
        value = node.value_of_css_property('font-size')  # return e.g:16px
        value = float(re.sub("[a-zA-Z]", "", str(value)))  # return e.g:16
        if value < 2:
            hidden_node.append(node)
            hidden_node_dict[Node.get_url(node)] = '2'
            return False

        # 3 检测visibility属性 {visible,hidden}
        value = node.value_of_css_property('visibility')
        if value == "hidden":
            hidden_node.append(node)
            hidden_node_dict[Node.get_url(node)] = '3'
            return False

        # 4 检测color属性{rgba(255, 255, 255, 1)}白色
        color = node.value_of_css_property('color')
        if color == "rgba(255, 255, 255, 1)":
            hidden_node.append(node)
            hidden_node_dict[Node.get_url(node)] = '4'
            return False

        # 5 检测opacity属性,透明度0.2以下即认为是暗链
        value = node.value_of_css_property('opacity')
        opacity = float(value)
        if opacity <= 0.2:
            hidden_node.append(node)
            hidden_node_dict[Node.get_url(node)] = '5'
            return False

        # 6 检测display属性{none,inline}
        value = node.value_of_css_property('display')
        if value == 'none':
            hidden_node.append(node)
            hidden_node_dict[Node.get_url(node)] = '6'
            return False

        '''
        若都符合上述特征，则对其父节点检测
        父节点已知属性
        "z-index": -1,
        "display": "none",
        "height": 0px,
        '''

        # 7检测父节点display属性{none,inline}
        value = node.find_element_by_xpath('..').value_of_css_property('display')
        if value == 'block':
            hidden_node.append(node)
            hidden_node_dict[Node.get_url(node)] = '7'
            return False

        # 8检测父节点属性text-indext()
        value = node.find_element_by_xpath('..').value_of_css_property('text-indent')
        value = float(re.sub(r'[a-zA-Z]', "", str(value)))
        if value < 0:
            hidden_node.append(node)
            hidden_node_dict[Node.get_url(node)] = '8'
            return False
        return False
