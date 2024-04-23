import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NYTimesSpider(CrawlSpider):
    name = 'nytimes'
    allowed_domains = ['nytimes.com']

    def _init_(self, seed_url=None, max_pages=10, max_depth=3, *args, **kwargs):
        super(NYTimesSpider, self)._init_(*args, **kwargs)
        self.start_urls = [seed_url] if seed_url else []
        self.max_pages = int(max_pages)
        self.max_depth = int(max_depth)

    rules = (
        Rule(LinkExtractor(allow=r'/2024/04/0[6-7]/'), callback='parse_article', follow=True),
    )

    def parse_article(self, response):
        # Extracting headline and article text
        headline = response.css('h1::text').get()
        article_paragraphs = response.css('p.Normal::text').getall()
        article_text = ' '.join(article_paragraphs)

        yield {
            'headline': headline,
            'article_text': article_text
        }