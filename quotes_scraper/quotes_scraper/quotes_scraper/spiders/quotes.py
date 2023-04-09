import scrapy

'''
Expresiones:
title = '//div/h1/a/text()'
citas = '//span[@class = "text" and @itemprop="text"]/text()'
autor = '//span/small/text()
top ten = '//span[@class = "tag-item"]/a/text()'
next page = '//li[@class = "next"]/a/@href'

'''

# Definir spider


class QuotesSpider(scrapy.Spider):
    # nombre del spider
    name = "quotes"
    # urls a las que se va a acceder
    start_urls = [
        "http://quotes.toscrape.com/page/1/",
    ]
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    #! recibe como parámetro el listado de citas que se van a ir actualizando

    def parse_quotes(self, response, **kwargs):
        if kwargs:
            citas = kwargs['quotes']
        citas.extend(response.xpath(
            '//span[@class = "text" and @itemprop="text"]/text()').getall())

        next_page_button = response.xpath(
            '//li[@class = "next"]/a/@href').get()
        if next_page_button:
            #! Vuelvo a pasar como parámetro al callback la lista de citas para que se vaya actualizando
            yield response.follow(next_page_button, callback=self.parse_quotes, cb_kwargs={'quotes': citas})
        else:
            #! Al llegar a la última página, devuelvo el listado de citas
            yield {
                'quotes': citas,
            }

    def parse(self, response):
        title = response.xpath('//div/h1/a/text()').get()
        citas = response.xpath(
            '//span[@class="text"]/text() | //span/small/text()').getall()
        top = response.xpath('//span[@class = "tag-item"]/a/text()').getall()
        top_number = getattr(self, 'number', None)
        if top_number:
            top = top[:int(top_number)]

        yield {
            'title': title,
            'top': top
        }

        next_page_button = response.xpath(
            '//li[@class = "next"]/a/@href').get()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse_quotes, cb_kwargs={'quotes': citas})
            #! Paso como parámetro al callback la lista de citas para que se vaya actualizando
