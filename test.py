#! /bin/python3



#import sys
#import importlib
#importlib.reload(sys)
import os
import re
import time

rootWeb="https://mateor.cn"
des="/home/cwj/Desktop/des/"
article_weblist=[]

def tra_weblist(website):
    if website in article_weblist:
        #print(website+"已访问过")
        return
    article_weblist.append(website)
    print(website)
    try:
        html=os.popen("curl "+website).read()   
    except:
        return
    if html.find("<span class=\"meta-nav\" aria-hidden=\"true\">上一篇</span>") != -1 or html.find("<span class=\"meta-nav\" aria-hidden=\"true\">下一篇</span>") != -1:#判断是否是文章
        art_flag=re.compile(r'<article id=[\u0000-\uFFFF]*?</article>')
        article_list=art_flag.findall(html)
        if len(article_list) == 1:#判断是否是文章
        #获取文章内容
            art_title_flag=re.compile(r'<h1 class="entry-title">([\u0000-\uFFFF]*?)</h1>')#获取标题
            art_title=re.search(art_title_flag,article_list[0]).group(1)
            #print(art_title)
            art_content_flag=re.compile(r'<div class="entry-content">([\u0000-\uFFFF]*?)</div>')#获取内容
            art_content=re.search(art_content_flag,article_list[0]).group(1)
            art_content=re.sub(r'<[\u0000-\uFFFF]*?>',"",art_content)
            art_content=re.sub(r'\n\n',"\n",art_content)
            if re.search(r'<time class="entry-date published" datetime=[\u0000-\uFFFF]*?>([\u0000-\uFFFF]*?)</time>',article_list[0]):
                art_bookmark_time=re.search(r'<time class="entry-date published" datetime=[\u0000-\uFFFF]*?>([\u0000-\uFFFF]*?)</time>',article_list[0]).group(1)
            elif re.search(r'<time class="entry-date published updated" datetime=[\u0000-\uFFFF]*?>([\u0000-\uFFFF]*?)</time>',article_list[0]):
                art_bookmark_time=re.search(r'<time class="entry-date published updated" datetime=[\u0000-\uFFFF]*?>([\u0000-\uFFFF]*?)</time>',article_list[0]).group(1)
            else :
                art_bookmark_time="unknown"
            if re.search(r'<a class="url fn n" href="[\u0000-\uFFFF]*?">([\u0000-\uFFFF]*?)</a>',article_list[0]):
                art_bookmark_author=re.search(r'<a class="url fn n" href="[\u0000-\uFFFF]*?">([\u0000-\uFFFF]*?)</a>',article_list[0]).group(1)
            else:
                art_bookmark_author="unknown"
            file=open(des+art_title+"_"+art_bookmark_author+"_"+art_bookmark_time+".txt","w")
            file.write("文章标题:"+art_title+"\n")
            file.write("作者："+art_bookmark_author+"     发布时间："+art_bookmark_time+"\n")
            file.write("来自："+website)
            file.write(art_content+"\n")
            file.close
            print("成功爬取文章《"+art_title+"_"+art_bookmark_author+"_"+art_bookmark_time+"》")
    #获取网址列表
    web_flag=re.compile(r'https://mateor.cn.*?"')
    weblist=web_flag.findall(html)
    #print(weblist)
    for i in range(0,len(weblist)):
        pos1=len(weblist[i])-1
        weblist[i]=weblist[i][0:pos1]
        tra_weblist(weblist[i])


tra_weblist(rootWeb)
    

