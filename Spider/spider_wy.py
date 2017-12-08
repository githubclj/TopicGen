import re
import urlparse
import urllib2
import time
from datetime import datetime
import robotparser
import bs4
import Queue
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import codecs


def get_allurl_from_js(js_url):
    try:
        html = urllib2.urlopen(js_url).read().decode('gbk')
    except:
        print "~~"

    pattern1 = '\"docurl\"\:\"http://tech\.163\.com/(.*)\",'  # okokoko~~~~~~~~~~~~~~~~~~~`
    webpage_regex = re.compile(pattern1, re.IGNORECASE)
    return webpage_regex.findall(html)
    # print len(webpage_regex.findall(html))
    # print webpage_regex.findall(html)


def get_latest_news(max_num, crawl_queue):
    url_count = 0
    js_index = 1
    while url_count < max_num:
        if js_index < 2:
            js_url = 'http://tech.163.com/special/00097UHL/smart_datalist.js?callback=data_callback'
            print js_url
        else:
            js_url = 'http://tech.163.com/special/00097UHL/smart_datalist' + '_0' + str(
                js_index) + '.js?callback=data_callback'
            print js_url
        links = get_allurl_from_js(js_url)
        js_index += 1
        for link in links:
            crawl_queue.append('http://tech.163.com/' + link)
            url_count += 1
            if url_count == max_num:
                break


def parse_html(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    title = (soup.title.string)[0:-5]
    content = ((soup.find('div', attrs={'class': 'post_text'})).get_text()).replace('\n', '')
    return title, content


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp',
                 proxy=None, num_retries=1):
    """Crawl from the given seed URL following links matched by link_regex
    """
    # the queue of URL's that still need to be crawled
    print "-----------seed_url--------------%s" % seed_url
    crawl_queue = Queue.deque([seed_url])
    # print crawl_queue.
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    # num_urls = 0
    rp = get_robots(seed_url)
    print rp
    throttle = Throttle(delay)
    headers = headers or {}
    # links = get_allurl_from_js('http://tech.163.com/special/00097UHL/smart_datalist.js?callback=data_callback')
    # for link in links:
    #     crawl_queue.append(link)
    get_latest_news(max_urls, crawl_queue)

    # crawl_queue.append(links)

    if user_agent:
        headers['User-agent'] = user_agent
    title_file = codecs.open("data/raw_title.txt", "a+")
    conte_file = codecs.open("data/raw_content.txt", "a+")
    url_file = codecs.open("data/url.txt", "a+")

    while crawl_queue:
        url = crawl_queue.pop()
        # print url
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)

            if url != 'http://tech.163.com/smart':
                title, content = parse_html(html)
                title_file.write(title + "\n")
                conte_file.write(content + '\n')
                url_file.write(url + '\n')
                # print html
                # links = []
                # depth = seen[url]
                # if depth != max_depth:
                #     # can still crawl further
                #     if link_regex:
                #         # filter for links matching our regular expression
                #         links.extend(link for link in get_links(html) if re.match(link_regex, link))
                #
                #     for link in links:
                #         # print link
                #         link = normalize(seed_url, link)
                #         # check whether already crawled this link
                #         if link not in seen:
                #             seen[link] = depth + 1
                #             # check link is within same domain
                #             if same_domain(seed_url, link):
                #                 # success! add this new link to queue
                #                 crawl_queue.append(link)

                # check whether have reached downloaded maximum
                # num_urls += 1
                # if num_urls == max_urls:
                #     break
        else:
            print 'Blocked by robots.txt:', url
    title_file.close()
    conte_file.close()


class Throttle:
    """Throttle downloading by sleeping between requests to same domain
    """

    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()


def download(url, headers, proxy, num_retries, data=None):
    print 'Downloading:', url
    request = urllib2.Request(url, data, headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        response = opener.open(request)
        html = response.read().decode('gbk')
        code = response.code
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                # retry 5XX HTTP errors
                return download(url, headers, proxy, num_retries - 1, data)
        else:
            code = None
    return html


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link)  # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # webpage_regex = re.compile('https?://\w+\.\w+\.\w+', re.IGNORECASE)

    # # list of all links from the webpage
    return webpage_regex.findall(html)
    # linklist={}
    # soup = bs4.BeautifulSoup(html, 'html.parser')


if __name__ == '__main__':
    # link_crawler('http://example.webscraping.com', '/(index|view)', delay=0, num_retries=1, user_agent='BadCrawler')
    link_crawler('http://tech.163.com/smart', 'http://tech\.163\.com/17/\d+?/\d+?/(.*)', delay=0, num_retries=1,
                 max_depth=1,
                 user_agent='GodCrawler', max_urls=100)
    # http: // fj\.people\.com\.cn / n /\d +? / \d +? / c\d +?-\d +?\.html
    # print re.match('http://tech\.163\.com/17/1124/08/^.{16,16}$/\.html', 'http://tech.163.com/17/1124/08/D409K9SL00097U7T.html')
    # print re.match('http://tech\.163\.com/17/\d+?/\d+?/(.*)', 'http://tech.163.com/17/1124/08/D409K9SL00097U7T.html')
