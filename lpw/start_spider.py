#当前完成了对于爬取中，URL规则的设置，爬取规则的设置，更新代理的设置，并且能够在DOWNLOAD_DELAY = 1的条件下进行爬取
#在DOWNLOAD_DELAY = 0.5时会遇到statu=302的错误，该错误是由于当前帐号访问量过多而引起的逻辑验证码问题，经过分析得到网站封的是账号行为不是IP行为，所以需要用机器学习的知识来进行解码，准备买
#早期数据暂时储存在文件中，后期将改为异步数据库存储
#备注：IP代理操作时需要在极光代理网进行白名单登记


from scrapy import cmdline

cmdline.execute("scrapy crawl lpw_spider".split(" "))