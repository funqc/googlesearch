# -*- coding: utf-8 -*-

import newspaper

from newspaper import Article

url = 'http://www.sciencedirect.com/science/article/pii/S0021999116304594'
article = Article(url)
article.download()
print (article.html.encode('utf-8'))
article.parse()
print (article.authors)