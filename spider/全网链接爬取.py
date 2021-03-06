# -*- coding:utf-8 -*-
import urllib2
import re
import time
import urlparse
import robotparser


def download(url, user_agent='wswp', try_numbers=2, proxy=None):
    print 'trying Downloading...', url
    header = {'user_agent': user_agent}
    request = urllib2.Request(url, headers=header)
    opener = urllib2.build_opener()
    if proxy:
        """支持代理"""
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = urllib2.urlopen(request).read()
        time.sleep(1)
    except urllib2.URLError, e:
        print 'Download error', e
        html = None
        if try_numbers > 0:
            if hasattr(e, 'code') and 500 <= e.code <= 600:
                return download(url, try_numbers=try_numbers-1)
    return html


def get_all_links(url):
    """获取当前url下所有的链接，去重处理"""
    content = download(url)
    reg = '<a.*?href="(.*?)".*?</a>'
    pat = re.compile(reg, re.S)
    links = re.findall(pat, content)
    unique_links = []
    for link in links:
        if 'http://' in link:
            links.remove(link)
        elif 'javascript' in link:
            links.remove(link)
        else:  # 去重
            full_link = urlparse.urljoin(url, link)
            if full_link not in unique_links:
                unique_links.append(full_link)
    print unique_links
    return unique_links


def robots_check(url, user_agent):
    """robot.txt检查，避免下载禁止爬取的代理"""
    robot_path = url + 'robots.txt'
    rp = robotparser.RobotFileParser()
    rp.set_url(robot_path)
    rp.read()
    return rp.can_fetch(user_agent, url)


def crawler(url):
    crawler_link = [url]
    seen_link = set(crawler_link)
    while crawler_link:
        link = crawler_link.pop()
        if robots_check(url, user_agent='user_agent'):  # 增加robot.txt检查，避免下载禁止爬取的代理
            all_links = get_all_links(link)
            for return_link in all_links:
                if urlparse.urljoin(url, '/') in return_link:  # 去除外网链接
                    if return_link not in seen_link:
                        seen_link.add(return_link)
                        crawler_link.append(return_link)
                        print '\n'
                        print '*' * 50 + return_link + '*' * 50
                    else:
                        print '%s is in the list!!!!!!!' % return_link
        else:
            print 'Blocked by robots.txt:', url
    print 'running over!!!!!!!!!!!!!!'


if __name__ == '__main__':
    crawler('http://www.b5cai.com/')
