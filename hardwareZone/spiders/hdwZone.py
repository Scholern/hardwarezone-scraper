# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json


class HdwzoneSpider(scrapy.Spider):
    name = 'hdwZone'
    allowed_domains = ['forums.hardwarezone.com.sg']
    start_urls = ['http://forums.hardwarezone.com.sg/']

    #Parse home page and get urls to posts
    def parse(self, response):
        table = response.css("#forum > table")[2]
        urls = table.css("tbody > tr > td:nth-child(2) > div > a::attr(href)").extract()
        for url in urls:
            url = response.urljoin(url)
            if "forums.hardwarezone.com.sg" in url:
                yield scrapy.http.Request(url, callback=self.parsePostPages)

    def parsePostPages(self, response):
        threads = response.css('#threadslist > tbody:nth-child(2) > tr')
        for thread in threads:
            continue
            threadUrl = thread.css('td:nth-child(3) > div > a::attr(href)').extract_first()
            yield scrapy.Request(url=response.urljoin(threadUrl), callback=self.parseThreads)
        
        next_page_url = response.css("#forum > table:nth-last-child(9) > tr > td:nth-child(2) > div > ul > li:nth-last-child(2) > a::attr(href)").extract_first()
        print response.url , next_page_url
        next_page_url = response.urljoin(next_page_url)
        return
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parsePostPages)
    

    #Parse 
    def parseThreads(self, response):
        print response.url
        title = response.css("#forum > h2::text").extract_first()
        category = response.css('#breadcrumbs > li:nth-child(4) > a::text').extract_first()
        thread_url = response.url
        posts = response.css("#posts > div")
        for post in posts:
            post_url = post.css("table > tr:nth-child(1) > td:nth-child(2) > a::attr(href)").extract_first()
            if post_url is None:
                continue
            item = {
                #Thread specific stuff (to identify the meta data)
                "title": title,
                "category": category,
                "updated_at": datetime.utcnow(),
                "thread_url": thread_url,
                #Post specific stuff
                "user" : {
                    "id" : post.css('table > tr:nth-child(2) > td:nth-child(1) > div:nth-child(1) > a::text').extract_first(),
                    "url" : post.css('table > tr:nth-child(2) > td:nth-child(1) > div:nth-child(1) > a::attr(href)').extract_first(),
                    "number_of_posts" : post.css('table > tr:nth-child(2) > td:nth-child(1) > div:nth-child(4) >div:nth-child(3)::text').extract_first()
                },
                "post": {
                    "post_time" : " ".join(post.css("table > tr:nth-child(1) > td:nth-child(1)::text").extract()).strip(),
                    "content" : post.css('table > tr:nth-child(2) > td:nth-child(2)').extract_first(),
                    "post_number" : post.css("table > tr:nth-child(1) > td:nth-child(2) > a >strong::text").extract_first(),
                    "post_url" : post_url
                }
            }
            yield item
        next_page_url = response.css("#forum > table:nth-child(15) > tr > td:nth-child(2) > div > ul > li:nth-child(11) > a::attr(href)").extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parseThreads)