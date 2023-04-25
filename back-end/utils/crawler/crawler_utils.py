from utils.crawler import crawler_driver
from utils.crawler.rules import AAAI, arxiv, cvpr, acm, sciencedirect, springer, IEEE


def get_abstract_by_crawler(url):
    try:
        # browser是一个webdriver对象，用于获取网页源代码
        browser = crawler_driver.init_driver(url)
        # c_url是当前网页的网址
        c_url = browser.current_url
        # 如果是 IEEE 的网址
        if c_url.find('ieee.org') != -1:
            res = IEEE.get_abstract(browser)
            return res
        # 如果是 ACM 的网址
        elif c_url.find('dl.acm.org') != -1:
            res = acm.get_abstract(browser)
            return res
        # 如果是 arxiv 的网址
        elif c_url.find('arxiv.org') != -1:
            res = arxiv.get_abstract(browser)
            return res
        # 如果是 science direct 的网址
        elif c_url.find('sciencedirect.com') != -1:
            res = sciencedirect.get_abstract(browser)
            return res
        # 如果是 springer 的网址
        elif c_url.find('springer.com') != -1:
            res = springer.get_abstract(browser)
            return res
        # 如果是 CVPR 网址
        elif c_url.find('thecvf.com') != -1:
            res = cvpr.get_abstract(browser)
            return res
        # 如果是 AAAI 网址
        elif c_url.find('aaai.org') != -1:
            res = AAAI.get_abstract(browser)
            return res
        # 如果是其他网址
        else:
            print('未收录网址：{}'.format(url))
            return ''
    except Exception as e:
        # 如果出现异常，打印异常信息
        print('错误：{}\n异常网址：{}'.format(e, url))
        return ''


if __name__ == '__main__':
    url0 = 'https://doi.org/10.48550/arXiv.2303.09607'
    print(get_abstract_by_crawler(url0))
