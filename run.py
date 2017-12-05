from urllib import request
import urllib
import numpy as np
import re
import requests 
# get the html of nips papers list and seve them in .npy
def get_html():
    f = request.urlopen('https://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017')
    data = f.read()
    html = data.decode('utf-8')
    np.save("html.npy", html)

# from the html code get the nips paper list    
def get_list(html):
    paper_list = []
    pattern = re.compile(r'<li><a href="/paper.*</a></li>')
    list = pattern.findall(html)
    for info in list:
        paper = get_info(info)
        paper_list.append(paper)
    return paper_list
    
def get_info(info):
    r_url = re.compile(r'<li><a href=".*</a> <a href=')
    re_url = r_url.findall(info)
    #print(url[0])
    str_url_start = '/paper/'
    str_url_end = '">'

    url_start = re_url[0].find(str_url_start)
    url_end = re_url[0].find(str_url_end)
    url = re_url[0][url_start:url_end]
    title = re_url[0][url_end+2:-13]
    
    r_author = re.compile(r'>[a-zA-Z\s*]+</')
    re_author = r_author.findall(info)
    author = ""
    for i in re_author:
        i = i[1:-2]
        author = author + ',' + i
    author = author[1:]
    #print(author)
    #info = [url,title,author]
    return ['https://papers.nips.cc'+url+'.pdf',title,author]
def write_downland_links(paper_list):
    f = open('list.txt','w+')
    list = []
    for link in paper_list:
        l = link[0] + '\n'
        list.append(l)
    f.writelines(list)
    f.close()

#get_html()
html = str(np.load('html.npy'))
paper_list = get_list(html)
#print(len(paper_list))
#write_downland_links(paper_list)
l = []
for i in range(len(paper_list)):
    info = "|"
    info += str(i+1)
    info += '|'
    info += '[' + paper_list[i][1] + ']'
    info += '(' + paper_list[i][0] + ')'
    info += '|'
    info += paper_list[i][2]
    info += '|' + '\n'
    l.append(info)
f = open('table.txt','w+')
f.writelines(l)
f.close()

