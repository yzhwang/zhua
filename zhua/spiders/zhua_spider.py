from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.selector import Selector

loginfo = open("forum.loginfo", "r").readline().split()
uid = loginfo[0]
pwd = loginfo[1]

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
            self.log("Login failed you sucker")
        else:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin.
            for url in self.start_urls:
                yield Request(url, callback=self.parse)
        
    def parse_posts(self, response):
        hxs = Selector(response)
        """links = hxs.xpath('//a[contains(@href, "topic")]')
        for link in links:
            title = ''.join(link.xpath('./@title').extract())
            url = ''.join(link.xpath('./@href').extract())
            meta={'title':title,}
            yield Request(url, callback = self.parse_items, meta=meta,)"""
        nextlink = hxs.xpath('//a[contains(@title, "Next page")]')
        url = ''.join(nextlink.xpath('./@href').extract())
        nexturl = url[len(url)/2:]
        print 'url: ' + response.url

    parse_start_url = parse_posts

    def parse_items(self, response):
        filename = 'download/'+ response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)

