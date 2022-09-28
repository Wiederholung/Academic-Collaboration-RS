import urllib.request
from xml.dom.minidom import parse
import DB.Utils.updateUtils as updateUtils
import crawler.crawlerUtils


def get_xml(url):
    return parse(urllib.request.urlopen(url))


def get_pid(name_en):
    url = 'https://dblp.uni-trier.de/search/author?xauthor=' + name_en
    xml = get_xml(url)
    root = xml.documentElement
    return root.getElementsByTagName('author')[0].getAttribute('pid')


def get_dblp_pub(pid):
    url = 'https://dblp.org/pid/' + pid + '.xml'
    xml = get_xml(url)
    return xml


# TODO: 获取所有需要的 abstract 信息 @胡 @川泽


def xml_browser(xml):
    # 获取根节点
    root = xml.documentElement

    # 最终返回的字典
    result = {'id': root.getAttribute('pid'), 'name': root.getAttribute('name'), 'Article': {}}

    # 获取合作者信息
    # 遍历每个合作文章
    in_proceedings = root.getElementsByTagName('inproceedings')
    for paper in in_proceedings:
        result = paper_manager(paper, result)

    articles = root.getElementsByTagName('article')
    for paper in articles:
        result = paper_manager(paper, result)
    return result


# 处理每一个 paper 节点，article 和 in_proceeding
def paper_manager(paper, result):
    # 获取key值
    article_name = paper.getAttribute('key')
    result['Article'][article_name] = {}
    # 获取title
    try:
        result['Article'][article_name]['title'] = paper.getElementsByTagName('title')[0].childNodes[0].data
    except Exception as e:
        print(e)
        result['Article'][article_name]['title'] = ''
    # 获取url
    try:
        result['Article'][article_name]['url'] = paper.getElementsByTagName('ee')[0].childNodes[0].data
    except Exception as e:
        print(e)
        result['Article'][article_name]['url'] = ''
    # 获取year
    try:
        result['Article'][article_name]['year'] = paper.getElementsByTagName('year')[0].childNodes[0].data
    except Exception as e:
        print(e)
        result['Article'][article_name]['year'] = ''
    # 获取合作者
    result['Article'][article_name]['author'] = {}
    for i in range(0, len(paper.getElementsByTagName('author'))):
        try:
            result['Article'][article_name]['author'][paper.getElementsByTagName('author')[i].childNodes[0].data] = \
                paper.getElementsByTagName('author')[i].getAttribute('pid')
        except Exception as e:
            print(e)
            result['Article'][article_name]['author'][
                paper.getElementsByTagName('author')[i].childNodes[0].data] = ''
    # 获取摘要
    try:
        result['Article'][article_name]['abstract'] = crawler.crawlerUtils.get_abstract(
            result['Article'][article_name]['url'])
    except Exception as e:
        print(e)
        result['Article'][article_name]['abstract'] = ''
    # print(result['Article'][article_name])
    return result


if __name__ == '__main__':
    n_list = updateUtils.get_all_col()
    for col in n_list[53:]:
        dblp_id = get_pid(col)
        dblp_xml = get_dblp_pub(dblp_id)
        json = xml_browser(dblp_xml)
        updateUtils.insert_pid(col, json)