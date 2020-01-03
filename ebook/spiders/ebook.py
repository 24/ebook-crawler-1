import scrapy


class PTTSpider(scrapy.Spider):
    name = 'ebook'
    allowed_domains = ['fast8.com']
    start_urls = (
        'http://www.fast8.com/list/8_1.html',
        'http://www.fast8.com/list/38_1.html',
        'http://www.fast8.com/list/39_1.html',
        'http://www.fast8.com/list/7_1.html',
        'http://www.fast8.com/list/35_1.html',
        'http://www.fast8.com/list/36_1.html',
        'http://www.fast8.com/list/37_1.html',
        'http://www.fast8.com/list/40_1.html',
        'http://www.fast8.com/list/41_1.html',
        'http://www.fast8.com/list/42_1.html',
    )

    def parse(self, response):
        title_set = set()
        for book_table in response.css('table.tablebordercss tr td[valign=top] table'):
            title = book_table.css("a::attr(title)").get()
            if not title:
                continue
            title = title.strip()
            if title in title_set:
                continue
            title_set.add(title)

            link = book_table.css("a::attr(href)").get() or ""
            if not link:
                continue
            link = link.strip()

            date = book_table.css("div font::text").get() or ""
            introduction = book_table.css("p font::text").get() or ""
            info = book_table.css("div::text").getall()
            info = [item.strip() for item in info]
            info = [item for item in info if item]

            language = ""
            size = ""
            popularity = ""
            if len(info) == 3:
                (language, size, popularity) = info
                language = language.strip("语言：")
                size = size.strip("大小：")
                popularity = popularity.strip("人气：")

            yield {
                'name': title,
                'link': response.urljoin(link),
                'date': date.strip(),
                'introduction': introduction.strip(),
                'language': language.strip(),
                'size': size.strip(),
                'popularity': popularity.strip(),
            }

        next_page = response.css("div.epages a:contains('下一页')::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            # print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
