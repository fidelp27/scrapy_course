import scrapy

class ScrapyLoginSpider(scrapy.Spider):
    name = 'scrapy_login'
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
    
    
    def start_requests(self):
        return [scrapy.FormRequest("http://quotes.toscrape.com/login",
                                   formdata={'username': 'fidelp27', 'password': 'Ezequie29.'},
                                   callback=self.logged_in)]
    
    def logged_in(self, response):
        # here you would extract links to follow and return Requests for
        # each of them, with another callback    
        quote = response.xpath('//div[@class="quote"]/span[@class="text"]/text()').getall()
        author = response.xpath('//div[@class="quote"]/span/small[@class="author"]/text()').getall()
                
        next_page_button = response.xpath(
            '//li[@class = "next"]/a/@href').get()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse, cb_kwargs={'quote': quote, 'author': author})
            #! Paso como parámetro al callback la lista de citas para que se vaya actualizando



    def parse(self, response, **kwargs):
        if kwargs:
            quote = kwargs['quote'] 
            author = kwargs['author']
        quote.extend(response.xpath('//div[@class="quote"]/span[@class="text"]/text()').getall())
        author.extend(response.xpath('//div[@class="quote"]/span/small[@class="author"]/text()').getall())
        
        next_page_button = response.xpath(
            '//li[@class = "next"]/a/@href').get()
        if next_page_button:
            #! Vuelvo a pasar como parámetro al callback la lista de citas para que se vaya actualizando
            yield response.follow(next_page_button, callback=self.parse, cb_kwargs={'quote': quote, 'author': author})
        else:
            #! Al llegar a la última página, devuelvo el listado de citas
            
            for quote, author in list(zip(quote, author)):
                yield {'quote': quote, 'author': author}
                
            
        
        
