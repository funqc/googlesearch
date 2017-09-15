# coding=utf-8
from __future__ import print_function
from pprint import pprint

from google import google
from trie import Trie
num_page = 10


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
import csv

with open('data.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        link = row[1]
        tree.insert(link)

f.close()
print('加载trie完成')

f = open('data.csv', 'a')
for line in open("keywords.txt"):
    line = line.decode('utf-8')
    if len(line) < 1:
        continue

    search_results = google.search(line, num_page)

    for result in search_results:
        link = result.link
        if tree.find(link):
            print('duplicate')
            continue
        tree.insert(result.link)
        res = result.name+','+result.link+"\n"#

        print(result.link)
        f.write(res.encode('utf-8'))
        # break

f.close()