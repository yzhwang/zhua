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
    login_page = 'https://www.depressionforums.org/forums/login/'
    start_urls = ['https://www.depressionforums.org/forums/forum/2-suicide-help-please-read-this-if-you-or-someone-you-know-are-having-thoughts-about-suicide-call-1-800-273-talk-8255-calls-are-connected-to-a-certified-crisis-center-nearest-the-callers-location/',
				  'https://www.depressionforums.org/forums/forum/79-forum-announcements/',
				  'https://www.depressionforums.org/forums/forum/10-a-special-forum-to-welcome-our-new-members/',
				  'https://www.depressionforums.org/forums/forum/7-our-forums-terms-of-service-tos-faq/',
				  'https://www.depressionforums.org/forums/forum/103-abilify-aripiprazole/',
				  'https://www.depressionforums.org/forums/forum/55-celexa-citalopram-lexapro-escitalopram/',
				  'https://www.depressionforums.org/forums/forum/50-cymbalta-duloxetine/',
				  'https://www.depressionforums.org/forums/forum/54-effexor-venlafaxine-pristiq-desvenlafaxine/',
				  'https://www.depressionforums.org/forums/forum/106-latuda-lurasidone/',
				  'https://www.depressionforums.org/forums/forum/57-paxilseroxat-paroxetine/',
				  'https://www.depressionforums.org/forums/forum/52-prozac-fluoxetine/',
				  'https://www.depressionforums.org/forums/forum/51-remeron-mirtazapine/',
				  'https://www.depressionforums.org/forums/forum/102-viibryd-vilazodone/',
				  'https://www.depressionforums.org/forums/forum/56-wellbutrin-bupropion/',
				  'https://www.depressionforums.org/forums/forum/53-zoloftlustral-sertraline/',
				  'https://www.depressionforums.org/forums/forum/46-other-depression-and-anxiety-medications/',
				  'https://www.depressionforums.org/forums/forum/39-medications-posting-asking-and-sharing/',
				  'https://www.depressionforums.org/forums/forum/11-mnesn-members-needing-extra-support-now/',
				  'https://www.depressionforums.org/forums/forum/12-depression-central/',
				  'https://www.depressionforums.org/forums/forum/32-anxiety-panic-post-traumatic-stress-disorders-ptsd/',
				  'https://www.depressionforums.org/forums/forum/112-dissociative-disorders/',
				  'https://www.depressionforums.org/forums/forum/38-attention-deficit-hyperactivity-disorder-adhdadd/',
				  'https://www.depressionforums.org/forums/forum/94-suicidal-ideation-forum/',
				  'https://www.depressionforums.org/forums/forum/105-anhedonia/',
				  'https://www.depressionforums.org/forums/forum/43-bereavement/',
				  'https://www.depressionforums.org/forums/forum/31-bipolar-disorder/',
				  'https://www.depressionforums.org/forums/forum/41-eating-disorders/',
				  'https://www.depressionforums.org/forums/forum/33-obsessive-compulsive-disorder-ocd/',
				  'https://www.depressionforums.org/forums/forum/34-personality-and-mental-health-disorders/',
				  'https://www.depressionforums.org/forums/forum/82-self-injury-si/?passForm=1',
				  'https://www.depressionforums.org/forums/forum/36-substance-abuse-recovery/?passForm=1',
				  'https://www.depressionforums.org/forums/forum/92-co-dependency/',
				  'https://www.depressionforums.org/forums/forum/37-other-depressive-health-disorders/',
				  'https://www.depressionforums.org/forums/forum/111-borderline-and-psychotic-symptoms/',
				  'https://www.depressionforums.org/forums/forum/14-the-relationship-and-depression-forum/',
				  'https://www.depressionforums.org/forums/forum/110-depression-and-families/',
				  'https://www.depressionforums.org/forums/forum/15-parents-and-childrens-depression-central/',
				  'https://www.depressionforums.org/forums/forum/81-depressed-and-bipolar-children/',
				  'https://www.depressionforums.org/forums/forum/93-depressed-or-bipolar-moms-and-dads/',
				  'https://www.depressionforums.org/forums/forum/100-mental-health-families-and-caregivers/',
				  'https://www.depressionforums.org/forums/forum/17-the-depression-and-religion-forum/',
				  'https://www.depressionforums.org/forums/forum/16-gay-lesbian-bi-sexual-and-transgender-issues/',
				  'https://www.depressionforums.org/forums/forum/97-bullying-emotional-and-physical-abuse/',
				  'https://www.depressionforums.org/forums/forum/89-therapy/',
				  'https://www.depressionforums.org/forums/forum/84-mental-illness-and-stigma-coping-with-the-ridicule/',
				  'https://www.depressionforums.org/forums/forum/40-psych-education-101/',
				  'https://www.depressionforums.org/forums/forum/96-clinical-trials-connection-plus-more/',
				  'https://www.depressionforums.org/forums/forum/28-one-step-at-a-time/',
				  'https://www.depressionforums.org/forums/forum/59-mental-health-disability-benefits-usukca-insurance-parity-etc/']
    rules = (Rule(SgmlLinkExtractor(allow=(r'page/[0-9]+', r'topic/'), deny=(r'\?comment', r'\?tab', r'\?do'), unique=True), callback='parse_posts', follow=True),)
    f = open("log.txt", "w+")

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
			#post_title = selector.xpath(u'//h1//span[@class="ipsType_break ipsContained"]//span').extract()[0].split('>')[1]
			#post_title = post_title[:-6]
			#post_id = response.url.split('-')[0].split('/')[-1]
			#print 'scraping content from ' + post_title + ' ' + post_id
			json_str = selector.xpath(u'//script[@type="application/ld+json"][text()[contains(.,"headline")]]').extract()[0].strip() + '\n'
			self.f.write(json_str)

			# New a post_item
			#post_item = PostItem()
			# extract pid from url like: http://my.domain/topic/pidnumber-long-post-title
			#post_item['post_id'] = post_id
			#post_item['title'] = post_title
			#post_item['author'] = selector.xpath(u'//div[@class="desc lighter blend_links"]//span[@itemprop="name"]/text()').extract()[0].strip()

			#post_item['author'] = selector.xpath(u'//ul[@class="cAuthorPane_info ipsList_reset"]//img/@alt').extract()[0].strip()
			#post_item['time'] = selector.xpath(u'//div[@class="desc lighter blend_links"]//span[@itemprop="dateCreated"]/text()').extract()[0].strip()
			#post_item['comments'] = []

	        #loop over every post_wrap
			#iter = 0
			#author_list = selector.xpath(u'//div[@class="author_info"]//span[@itemprop="name"]/text()').extract()
			#comment_id_list = selector.xpath(u'//div[@class="post_wrap"]//@data-entry-pid').extract()
			#comment_time_list = selector.xpath(u'//div[@class="post_body"]//abbr[@class="published"]/text()').extract()
			#comment_text_list = selector.xpath(u'//div[@class="post_body"]//div[@itemprop="commentText"]').extract()

			#for comment in selector.xpath(u'//div[@class="post_wrap"]'):
			#	comment_item = CommentItem()
			#	comment_item['comment_id'] = comment_id_list[iter].strip()
			#	comment_item['author'] = author_list[iter].strip()
			#	comment_item['time'] = comment_time_list[iter].strip()
			#	comment_item['text'] = re.sub(r'<.+?>', '', comment_text_list[iter]).strip(' \n\t')
			#	post_item['comments'].append(comment_item)
			#	iter+=1
			#return post_item

    parse_start_url = parse_posts
