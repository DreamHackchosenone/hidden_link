# coding:utf-8
import re
import urllib

import time
from selenium import webdriver


class Node():
    def __init__(self, url):
        self.driver = webdriver.PhantomJS()
        self.url = url

    def parge_source(self):
        parge_source = self.driver.get(self.url)
        return parge_source

    def get_urlnode(self):
        '''
        每个节点对应一条url
        :param driver:
        :return:返回当前页面所有的url节点  type:tuple(node_list,url_list)
        '''
        self.driver.get(self.url)
        # time.sleep(2)  # 等待加载
        all_node = []  # 网页的src,href节点,可能包含非法url
        node_list = []  # 带有url的节点
        url_list = []  # 节点中的url
        all_node.extend(self.driver.find_elements_by_xpath(".//*[@href]"))
        all_node.extend(self.driver.find_elements_by_xpath(".//*[@src]"))
        http_pattern = re.compile(r'^(http).*')
        for node in all_node:
            url = node.get_attribute('href') or node.get_attribute('src')  # url引用分src和href
            if url is None:
                continue
            http_match = http_pattern.search(url)  # 可能抓取到一些非url
            if http_match:
                node_list.append(node)
                url_list.append(url)
            # 返回有url的node
            else:
                pass
        # with open('url.txt', 'w')as f:
        #     for i in url_list:
        #         f.write(i + '\n')
        return (node_list, url_list)

    def get_outdomainnode(self, urlnode, domain):
        node_list = urlnode[0]
        url_list = urlnode[1]
        i = 0
        while i < len(node_list):
            self.get_domain(url_list[i])
            if domain == self.get_domain(url_list[i]):
                node_list.pop(i)
                url_list.pop(i)
                i -= 1
            else:
                pass
            i += 1
        return node_list

    @staticmethod
    def get_domain(url):
        '''
        :return:
        '''
        protol, rest = urllib.splittype(url)
        domain, rest = urllib.splithost(rest)
        return domain

    @staticmethod
    def get_url(node):
        url = node.get_attribute('href') or node.get_attribute('src')
        return url

    @staticmethod
    def get_url_list(node_list):
        url_list = []
        for node in node_list:
            url = node.get_attribute('href') or node.get_attribute('src')
            url_list.append(url)
        return url_list

    @staticmethod
    def print_text(node_list):
        nodetext = []
        for node in node_list:
            text = node.text
            nodetext.append(text)
        return text

    def quit(self):
        self.driver.quit()

