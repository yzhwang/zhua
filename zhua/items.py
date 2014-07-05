# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class PostItem(Item):
    title = Field()
    author = Field()
    time = Field()
    comments = Field()

class CommentItem(Item):
    author = Field()
    gender = Field()
    location = Field()
    time = Field()
    text = Field()

