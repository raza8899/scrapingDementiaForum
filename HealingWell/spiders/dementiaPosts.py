import scrapy

class HealingWellScraperPostLink(scrapy.Spider):

    # name and start_urls are two required parameters, where the name has to be unique
    # the name is used to perform the crawling job, e.g scrapy crawl dementiaPosts 

    name="dementiaPosts"
    start_urls=["https://www.healingwell.com/community/default.aspx?f=8"]


    # This function is the main functions that parse the html code of the website

    def parse(self,response):
        for item in response.css('div.forum-list-row'):

            # we are using css selectors, where forum-title is class name
            title=item.css("a.forum-title::text").get()
            pageUrl="https://www.healingwell.com"+item.css("a.forum-title::attr(href)").get()

            # after retrieving the title and postURL we pass it to other function
            # the parse_nested_item takes the postURL and scrapes the user's query and all the comments

            yield scrapy.Request(url=pageUrl,meta={'title':title}, callback=self.parse_netsted_item)
        
        # now we check if there is next page available or not and call the whole function again
        
        next_page=response.css('span.page-listing-selected+a::attr(href)').get()
        next_page="https://www.healingwell.com"+next_page

        if next_page is not None:
            next_page=response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)
        
        


    def parse_netsted_item(self,response):

        title = response.meta['title']
        count=0
        userQuery=""
        comments=[]
        for eachitem in response.css("div.post-even"):
            query= eachitem.css("div.post-body").xpath(".//text()").extract()
            query=" ".join(query)
            query=query.strip()
            query=" ".join(query.split())

            if count==0:
                userQuery=query
                count=1
            else:
                comments.append(query)
        
        for eachitem in response.css("div.post-odd"):
            query= eachitem.css("div.post-body").xpath(".//text()").extract()
            query=" ".join(query)
            query=query.strip()
            query=" ".join(query.split())
            comments.append(query)

        if len(comments)==0:
            comments.append(" ")

        comments="\n\n\n ".join(comments)
        
      
        yield{
            'Title':title,
            'Query':userQuery,
            'Answers':comments
        }

