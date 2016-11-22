# -*- coding:utf-8 -*-
import urllib2
import re


def download(url, user_agent='wswp', try_numbers=2):
    print 'trying %d Downloading...' % try_numbers, url
    header = {'user_agent': user_agent}
    request = urllib2.Request(url, headers=header)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError, e:
        print 'Download error', e
        html = None
        if try_numbers > 0:
            if hasattr(e, 'code') and 500 <= e.code <= 600:
                return download(url, try_numbers-1)
    return html


def sitemap(url):
    pass


if __name__ == '__main__':
    # a = download('http://www.b5cai.com/')
    # print a
    pass
    a = download('http://www.b5cai.com/robots.txt')
    print a
    reg = 'Sitemap:(.*?)\n'
    pattern = re.compile(reg, re.S)
    b = re.findall(pattern, a)
    print b[0], type(b[0])
    c = download(b[0])
    reg2 = '<loc>(.*?)</loc>'
    pat = re.compile(reg2, re.S)
    links = re.findall(pat, c)
    print links
    for link in links:
        print link


