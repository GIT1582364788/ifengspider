# -*- coding: utf-8 -*-
import scrapy
from ifengspider.items import IfengspiderItem


class IfengSpider(scrapy.Spider):
    name = 'ifeng'
    allowed_domains = ['news.ifeng.com']        # 过滤爬取的域名 ['news.ifeng.com','guoxue.ifeng.com']
    start_urls = ['http://news.ifeng.com/ipad']

    def parse(self, response):
        categorys = response.xpath("//ul[@class='clearfix']/li/a/text()").extract()
        links = response.xpath("//ul[@class='clearfix']/li/a/@href").extract()
        # print(categorys,links)
        for category,link in zip(categorys,links):
            # item = IfengspiderItem()        # 实例化 import IfengspiderItem
            # item['category'] = category
            # item['link'] = link

            # 记录  标题  以及 标题链接
            data = {'category':category,'link':link}
            # 请求分类页面
            yield scrapy.Request(link,meta={'data':data},callback=self.getNewList)      # 请求每一个标题，链接

    def getNewList(self,response):      # response已经是国际里边的内容了,一级标题有几个就执行几次
        data = response.meta['data']        # 通过meta得到data
        # print(item)
        # print(item['category'])
        """
        国际
        name = //div[@class='juti_list']/h3/a/text()
        href = //div[@class='juti_list']/h3/a/@href
        
        即时
        name = //div[@class='newsList']/ul/li/a/text()
        href = //div[@class='newsList']/ul/li/a/@href
        
        大鱼漫画
        name = //div[@class='con_lis show']/a/text()
        href = //div[@class='con_lis show']/a/@href
        
        专题
        name = //ul[@class='clearfix']/li/a/text()
        href = //ul[@class='clearfix']/li/a/@href
        
        大陆
        name = //div[@class='juti_list']/h3/a/text()
        href = //div[@class='juti_list']/h3/a/@href
        
        排行
        name = //td/h3/a/text()
        href = //td/h3/a/@href
        
        """
        category = data['category']
        link = data['link']
        titles = []
        conlinks = []
        if category =='国际':
            titles += response.xpath("//div[@class='juti_list']/h3/a/text()").extract()  # 标题  国际
            conlinks += response.xpath("//div[@class='juti_list']/h3/a/@href").extract()  # 文章链接
        if category =='即时':
            titles += response.xpath("//div[@class='newsList']/ul/li/a/text()").extract()  # 标题   即时
            conlinks += response.xpath("//div[@class='newsList']/ul/li/a/@href").extract()  # 文章链接
        if category == '大鱼漫画':
            titles += response.xpath("//div[@class='con_lis show']/a/text()").extract()  # 标题   大鱼漫画
            conlinks += response.xpath("div[@class='con_lis show']/a/@href").extract()  # 文章链接
        if category == '专题':
            titles += response.xpath("//ul[@class='clearfix']/li/a/text()").extract()  # 标题   专题
            conlinks += response.xpath("//ul[@class='clearfix']/li/a/@href").extract()  # 文章链接
        if category == '大陆':
            titles += response.xpath("//div[@class='juti_list']/h3/a/text()").extract()  # 标题   大陆
            conlinks += response.xpath("//div[@class='juti_list']/h3/a/@href").extract()  # 文章链接
        if category =='排行':
            titles += response.xpath("//td/h3/a/text()").extract()  # 标题   排行
            conlinks += response.xpath("//td/h3/a/@href").extract()  # 文章链接
        if category =='台湾':
            titles += response.xpath("//div[@class='juti_list']/h3/a/text()").extract()
            conlinks += response.xpath("div[@class='juti_list']/h3/a/@href").extract()

        if titles and conlinks:
            for title,conlink in zip(titles,conlinks):
                item = IfengspiderItem()        # 实例化
                item['category'] = category
                item['link'] = link
                item['title'] = title
                item['conlink'] = conlink
                # print(item)
                yield scrapy.Request(conlink,meta={'item':item},callback=self.getNewCon)

    def getNewCon(self,response):
        item = response.meta['item']
        date = []
        author = []
        con = []
        if item['category'] == "国际":
            date += response.xpath("//p[@class='p_time']/span[1]/text()").extract()
            author += response.xpath("//span[@class='ss03']/a/text()").extract()
            con += response.xpath("//div[@id='artical_real']//text()").extract()
        if item['category'] == "即时":
            pass
        if item['category'] == "大陆":
            date += response.xpath("//p[@class='p_time']/span[1]/text()").extract()
            author += response.xpath("//span[@class='ss03']/a/text()").extract()
            con += response.xpath("//div[@id='artical_real']//text()").extract()
        if item['category'] == "台湾":
            date += response.xpath("//p[@class='p_time']/span[1]/text()").extract()
            author += response.xpath("//span[@class='ss03']/a/text()").extract()
            con += response.xpath("//div[@id='artical_real']//text()").extract()

        if date and author and con:
            item['con'] = con
            item['date'] = date
            item['author'] = author
        yield item










