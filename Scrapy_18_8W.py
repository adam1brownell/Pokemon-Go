import scrapy, re

class QuotesSpider(scrapy.Spider):
    name = "pokedex"
    
    def start_requests(self):    
        urls = [ 'https://fevgames.net/pokedex/' ]
        
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)
            
    def parse(self, response):
        #Build dictionary of pokemon num and name
        x = response.css('a.pokedex-item:first-child').re(r'<br>(\W*\w+)')
        #dtm = dict(x[i:i+1] for i in range(0,len(x),2))
        
        #build list of urls to visit
        lnx = response.css('a.pokedex-item:first-child').re(r'href=\"(.*)\"\>\<img')
        
        #There is probably a nicer way to do this, but I'm manually iter
        #through list of name/num to pass meta to correct link
        i = 0
        for link in lnx:
            newUrl = "https://fevgames.net" + link
            number = x[i]
            name = x[i+1]            
            request = scrapy.Request(url = newUrl, callback = self.parse2)
            
            request.meta["Number"] = number
            request.meta["Name"] = name
            i = i + 2
            yield request
    def parse2(self,response):
    
        x = response.css('#omc-full-article table tr:nth-child(2) td:nth-child(2)'
                        ).re(r'<td>(.*)</td>')
        dez = { "Number":response.meta["Number"],
                "Name": response.meta["Name"],
                "Description":x
              }
        return dez
        
""" 
filename = 'pokedex.csv'
        with open(filename, 'wb') as f:
            json.dump(pokelist, f)
"""