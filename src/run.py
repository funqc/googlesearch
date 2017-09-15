#!/usr/bin/python
# coding=utf-8

import logging
import os
import sys
import multiprocessing
import csv

import time

from trie import Trie
from google import google

from newspaper import Article


def googlesearch(inp, dirname, num_page=30):
    '''
    GoogleResult:
        self.name # The title of the link
        self.link # The link url
        self.description # The description of the link
        self.thumb # The link to a thumbnail of the website (not implemented yet)
        self.cached # A link to the cached version of the page
        self.page # What page this result was on (When searching more than one page)
        self.index # What index on this page it was on
    '''
    tree = Trie()
    urlfile = os.path.join(dirname, 'url.csv')
    textfile = os.path.join(dirname, 'text.txt')

    if os.path.exists(urlfile):
        temp = 0
        with open(urlfile, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                link = row[1]
                tree.insert(link)
                temp+=1
        f.close()
        if temp > 0:
            num_page = 3
        print('download trie completed, num_page=%d' % num_page)

    f = open(urlfile, 'a')
    for line in open(inp):
        line = line.decode('utf-8')
        if len(line) < 1:
            continue

        search_results = google.search(line, num_page)

        for result in search_results:
            link = result.link
            if tree.find(link):
                # print('duplicate')
                continue
            tree.insert(result.link)
            res = result.name + ',' + result.link + "\n"  #
            f.write(res.encode('utf-8'))
            article = Article(result.link)
            article.download()
            html = article.html
            with open(textfile, 'a') as textf:
                textstr = '%s\r\n%s\r\n\r\n' % (result.link, html)
                textf.write(textstr.encode('utf-8'))
            textf.close()
            # break
        time.sleep(10)
    f.close()


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 1:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    inp = sys.argv[1]

    dirname = inp.split('.')[0]
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        print('mkdir %s' % dirname)

    while 1:
        googlesearch(inp, dirname)
        time.sleep(86400)