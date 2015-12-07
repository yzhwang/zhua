from scrapy.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule
from scrapy.selector import Selector
from zhua.items import PostItem, CommentItem
import re


# Define a list of PostItem
post_items = []

loginfo = open("forum.loginfo", "r").readline().split()
uid = loginfo[0]
pwd = loginfo[1]

def GetFirst(iterable, default=None):
	for item in iterable:
		return item
	return default

class ZhuaSpider(CrawlSpider):
    name = 'zhuaspider'
    allowed_domains = ['depressionforums.org']
    login_page = 'http://www.depressionforums.org/forums/index.php?app=core&module=global&section=login'
    start_urls = ['http://www.depressionforums.org/forums/forum/12-depression-central/']

    rules = (
            Rule(SgmlLinkExtractor(allow=(r'page-[0-9]+', r'topic/'), unique=True), callback='parse_posts', follow=True),
    )

    def start_requests(self):
        """called before crawling starts. Try to login"""
        yield Request(
                url=self.login_page,
                callback=self.login,
                dont_filter=True)

    def login(self, response):
        """Generate a login request."""
        return FormRequest.from_response(response,
                formdata={'ips_username': uid, 'ips_password': pwd},
                callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are successfully logged in."""
        if "Username or password incorrect" in response.body:
            self.log("Login failed. Check your uid and pwd info in forum.loginfo")
        else:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin.
            for url in self.start_urls:
                yield Request(url, callback=self.parse)    

    def parse_posts(self, response):
        if 'topic/' in response.url:
        	print 'scraping content in url: ' + response.url
        	selector = Selector(response)
	        post_title = selector.xpath('//h1/text()').extract()[0]
	        post_id = response.url.split('-')[0].split('/')[-1]
	        # New a post_item
	        post_item = PostItem()
	        # extract pid from url like: http://my.domain/topic/pidnumber-long-post-title
	        post_item['post_id'] = post_id
	        post_item['title'] = post_title
	        post_item['author'] = selector.xpath(u'//div[@class="desc lighter blend_links"]//span[@itemprop="name"]/text()').extract()[0].strip()
	        post_item['time'] = selector.xpath(u'//div[@class="desc lighter blend_links"]//span[@itemprop="dateCreated"]/text()').extract()[0].strip()
	        post_item['comments'] = []

	        #loop over every post_wrap
	        iter = 0
	        author_list = selector.xpath(u'//div[@class="author_info"]//span[@itemprop="name"]/text()').extract()
	        comment_id_list = selector.xpath(u'//div[@class="post_wrap"]//@data-entry-pid').extract()
	        comment_time_list = selector.xpath(u'//div[@class="post_body"]//abbr[@class="published"]/text()').extract()
	        comment_text_list = selector.xpath(u'//div[@class="post_body"]//div[@itemprop="commentText"]').extract()

	        for comment in selector.xpath(u'//div[@class="post_wrap"]'):
	        	comment_item = CommentItem()
	        	comment_item['comment_id'] = comment_id_list[iter].strip()
	        	comment_item['author'] = author_list[iter].strip()
	        	comment_item['time'] = comment_time_list[iter].strip()
	        	comment_item['text'] = re.sub(r'<.+?>', '', comment_text_list[iter]).strip(' \n\t')
	        	post_item['comments'].append(comment_item)
	        	iter+=1
	        return post_item


    parse_start_url = parse_posts

    
        




