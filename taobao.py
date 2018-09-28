#encoding=utf8
import sys
import getopt
import time
import re
import requests
import json

def Usage():
    print ('艾斯卡尔  taobao-spider 使用指南:')
    print ('    -h    --help:    显示帮助信息.')
    print ('    -v    --ver:    显示脚本版本')
    print ('    -k    --key:    搜索关键词，默认 iphone7')
    print ('    -n    --num:    搜索页数，每页包含44条商品数据，如输入2，那说明会抓取2*44条商品数据')
    print ('    -f    --file:    获取的文件保存位置，默认为D:\iphone.txt')
    print ('使用实例：')
    print ('python taobao.py -k 滑板鞋 -n 5 -f D:\huaban.txt')
def Version():
    print ('python-spider 1.0.0')
def OutPut(args):
    print (str(args))
def OutPutKN(args):
    print (str(args))
class ProgressBar():
  def __init__(self, width=100):
    self.pointer = 0
    self.width = width
  def __call__(self,x,w):
     self.pointer = int(self.width*(x/w))
     return "|" + "#"*self.pointer + "-"*(self.width-self.pointer)+\
        "|\n %.2f %% 完成" % float((x/w)*100)
def spider(num,keyWord,fileName):
    if(num==0):
        num=1
    if(keyWord==""):
        keyWord="男子汉"
    if(fileName==""):
        fileName="D:\sex.txt"
    limit=num #爬取页数据，每页44个记录
    keystr=keyWord #搜索关键词
    url = 'https://s.taobao.com/search'
    rateUrl = 'https://rate.taobao.com/feedRateList.htm'
    tmrateUrl = 'https://rate.tmall.com/listTagClouds.htm'
    payload = {'q': keystr,'s': '1','ie':'utf8'}  #字典传递url参数，第二字段写要搜索的关键词
    rateload = {'auctionNumId': '44404493527','userNumId': '839556000','currentPageNum':'1','pageSize':'20','rateType':'1','folded':'0','ie':'utf8'}  #字典传递url参数
    tmrateload = {'itemId': '44404493527','isAll': 'true','isInner':'true','ie':'utf8'}  #字典传递url参数
    file = open(fileName,'w',encoding='utf-8') #可以指定文件名
    print ("爬数据开始，搜索关键词为："+keystr+" , 总共要爬的记录"+str(limit*44)+"条")
    for k in range(0,limit):
        payload ['s'] = 44*k+1   #此处改变的url参数为s，s为1时第一页，s为45是第二页，89时第三页以此类推
        resp = requests.get(url, params = payload)
        #print(resp.url)          #打印访问的网址
        resp.encoding = 'utf-8'  #设置编码
        title = re.findall(r'"raw_title":"([^"]+)"',resp.text,re.I)  #正则保存所有raw_title的内容，这个是书名，下面是价格，地址
        price = re.findall(r'"view_price":"([^"]+)"',resp.text,re.I)
        loc = re.findall(r'"item_loc":"([^"]+)"',resp.text,re.I)
        sales = re.findall(r'"view_sales":"([^"]+)"',resp.text,re.I)
        pid = re.findall(r'"nid":"([^"]+)"',resp.text,re.I)
        x = len(title)           #每一页商品的数量
        for i in range(0,x) :    #把列表的数据保存到文件中
            # haoping
            rateload ['auctionNumId'] = pid[i]
            rateload ['rateType'] = 1
            respRate = requests.get(rateUrl, params = rateload)
            respRate.encoding = 'utf-8'  #设置编码
            ratevalue = re.findall(r'"total":([^,]+)',respRate.text,re.I)
            pomax = re.findall(r'"maxPage":([^,]+)',respRate.text,re.I)
            positive=ratevalue[0]
            rateload ['rateType'] = 0
            respRate = requests.get(rateUrl, params = rateload)
            respRate.encoding = 'utf-8'  #设置编码
            ratevalue = re.findall(r'"total":([^,]+)',respRate.text,re.I)
            normax = re.findall(r'"maxPage":([^,]+)',respRate.text,re.I)
            middle=ratevalue[0]
            rateload ['rateType'] = -1
            respRate = requests.get(rateUrl, params = rateload)
            respRate.encoding = 'utf-8'  #设置编码
            ratevalue = re.findall(r'"total":([^,]+)',respRate.text,re.I)
            nemax = re.findall(r'"maxPage":([^,]+)',respRate.text,re.I)
            negative=ratevalue[0]
            #if middle == '0' and nemax[0] == '0':    # 判断是淘宝的还是天猫的
                #print ("我是天猫的，我运行了")
                #tmrateload ['itemId'] = pid[i]
                #tmrespRate = requests.get(tmrateUrl, params = tmrateload)
                #tmrespRate.encoding = 'utf-8'  #设置编码
                #json_str = json.dumps(tmrespRate.text)
                #json_data = json.loads(json_str)
                #print (json_str['tags']['tagClouds'][0]['count'])
            current=i+(k*44)
            allcount=limit*44
            pb = ProgressBar()
            print (pb(current,allcount))
            #print(" 第 " + str(current) + " 条商品数据 -- 总进度：" + str('%.2f'%((current/allcount)*100))+"%")
            try:
                file.write(str(k*44+i+1)+' 商品ID：'+pid[i]+' &&& '+' 商品名称：'+title[i]+' &&& '+'价格：'+price[i]+' &&& '+'地址：'+loc[i]+' &&& '+'销量：'+sales[i]+' &&& '+'好评：'+positive+' &&& '+'中评：'+middle+' &&& '+'差评：'+negative+'\n')
            except:
                file.write(str(k*44+i+1)+' 商品ID：'+pid[i]+' &&& '+' 商品名称：'+title[i]+' &&& '+'价格：'+price[i]+' &&& '+'地址：'+loc[i]+' &&& '+'销量：'+"0人付款"+' &&& '+'好评：'+positive+' &&& '+'中评：'+middle+' &&& '+'差评：'+negative+'\n')
    print (pb(1,1))
    file.close()
def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], 'hvk:n:f:', ['help', 'version', 'key=', 'num=', 'file='])
    except getopt.GetoptError:
        Usage()
        sys.exit(2)
    key =""
    num =0
    fileName=""
    for o, a in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit(1)
        elif o in ('-v', '--version'):
            Version()
            sys.exit(0)
        elif o in ('-k', '--key'):
            key=a
        elif o in ('-n', '--num'):
            num=int(a)
        elif o in ('-f', '--file'):
            fileName=a
        else:
            print ('unhandled option')
            sys.exit(3)
    spider(num,key,fileName)
if __name__ == '__main__':
    main(sys.argv)
