# Scrapy settings for zhua project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'zhua'

SPIDER_MODULES = ['zhua.spiders']
NEWSPIDER_MODULE = 'zhua.spiders'
ITEM_PIPELINES = ['zhua.pipelines.ZhuaPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhua (+http://www.yourdomain.com)'
