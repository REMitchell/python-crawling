
from scrapy import Item, Field


class Article(Item):
    title = Field()
    links = Field()
    lastModified = Field()