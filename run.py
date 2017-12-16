# coding: utf-8
from hidden_check.Node import Node
from hidden_check.Analyse import start, hidden_node_dict

URL = "http://www.gengjunfei.com"

def run():
    node = Node(URL)
    # 获取所有链接节点
    urlnode = node.get_urlnode()
    print Node.get_url_list(urlnode[0])
    # 获取当前url域名
    domain = node.get_domain(URL)
    # 获取外域节点
    outdomainnode = node.get_outdomainnode(urlnode, domain)
    print Node.get_url_list(outdomainnode)
    # 获取暗链节点
    hidden_node = start(outdomainnode)
    print Node.get_url_list(hidden_node)
    print hidden_node_dict
    node.quit()

if __name__ == "__main__":
        run()
