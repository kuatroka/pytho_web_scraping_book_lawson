# To add a new cell, type ' '
# To add a new markdown cell, type '  [markdown]'

 
import urllib.request
import pprint
def download(url):
    print(urllib.request.urlopen(url, context=ctx).read())
    # return urllib.request.urlopen(url).read()

# a = download('http://example.webscraping.com/places/default/index/1')
download('http://example.webscraping.com/places/default/index/1')


 
url = 'http://www.thebesttimetovisit.com/weather/maldives-idpaysglobaleng-90.html'
download(url)


 
urllib.request.urlopen('http://example.webscraping.com/places/default/index/1', context=ctx)


 
# a more robust version of the script
import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError

def download(url):
    print('Downloading:', url)
    try:
        html = urllib.request.urlopen(url).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
    return html

url = 'http://www.thebesttimetovisit.com/weather/maldives-idpaysglobaleng-90.html'
download(url)


 
url = 'https://score.accenture.com/WebPages/CollectionActivity.aspx'
download(url)


# **If the error is "503 Service Unavailable error" then we can retry downloading web page,
# but if it's "404 Not Foound" then it wouldn't make sense
# 


# Only retry download if the error starts with 5, ie 5xx, but not 4xx
import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError

def download(url, num_retries=2):
    print('Downloading:', url)
    try:
        html = urllib.request.urlopen(url).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Downloading error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
            
    return html

download('http://httpstat.us/500')


download('http://httpstat.us/400')


download('http://www.meetup.com/')


from pprint import pprint
print(download('http://www.meetup.com/'))

# ## Setting a user agent

def download(url, user_agent='wswp', num_retries=2):
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        html = urllib.request.urlopen(request).read()
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                ## resucrsively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html


print(download('http://www.meetup.com/'))

# ## Sitemap crawler - this one searches the robots.txt file and extracts all the site links from it

import re
import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError

def download(url, user_agent='wswp', num_retries=2, charset='utf-8'):
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:',  e.code, e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html

def crawl_sitemap(url):
    # download sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each link
    for link in links:
        html = download(link)
        # scrape html here



crawl_sitemap('http://example.webscraping.com/sitemap.xml')

# ## ID iteration crawler - this one searches without robots.txt file links

import itertools
def crawl_site(url):
    for page in itertools.count(1):
        # print(page)
        pg_url = f'{url}{page}'
        html = download(pg_url)
        if html is None:
            break
        # success - can scrape the result


crawl_site('http://example.webscraping.com/view/-')

# ## This one uses a failsafe of stopping after 5 consecutive errors

import itertools

def crawl_site(url, max_errors=5):
    num_errors = 0
    for page in itertools.count(1):
        print(f'itertsool.count(1) ...{page}')
        # print(page)
        pg_url = f'{url}{page}'
        html = download(pg_url)
        if html is None: # error occured
            num_errors += 1
            if num_errors == max_errors:
                # max errors reached, exit loop
                break
            else:
                num_errors = 0



        # success - can scrape the result


crawl_site('http://example.webscraping.com/view/-')

# ## Link crawler - with regex


import re
import urllib.request
from urllib.parse import urljoin
from urllib.error import URLError, HTTPError, ContentTooShortError


def download(url, num_retries=2, user_agent='wswp', charset='utf-8'):
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html


def link_crawler(start_url, link_regex):
    """ Crawl from the given start URL following links matched by
        link_regex
    """
    crawl_queue = [start_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        if not html:
            continue
        # filler for links matching our regex
        for link in get_links(html):
            if re.match(link_regex, link):
                abs_link = urljoin(start_url, link)
                if abs_link not in seen:
                    seen.add(abs_link)
                    crawl_queue.append(abs_link)



def get_links(html):
    """return a list of links from html"""
    # a regex to extract all links from the page
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list of all links from the page
    return webpage_regex.findall(html)


link_crawler('http://example.webscraping.com', '/(index|view|places)/')


link_crawler('https://www.zerohedge.com', '/markets/')


link_crawler('https://www.zerohedge.com', '')

# ## Parsing robots.txt file

from urllib import robotparser
rp = robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
rp.read()
rp


url = 'http://example.webscraping.com/robots.txt'
user_agent = 'BadCrawler'
rp.can_fetch(user_agent, url)


user_agent = 'GoodCrawler'
rp.can_fetch(user_agent, url)

#######################################

import re
import urllib.request
from urllib import robotparser
from urllib.parse import urljoin
from urllib.error import URLError, HTTPError, ContentTooShortError


def download(url, num_retries=2, user_agent='wswp', charset='utf-8'):
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        resp = urllib.request.urlopen(request, context=ctx)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html

def get_links(html):
    """return a list of links from html"""
    # a regex to extract all links from the page
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list of all links from the page
    return webpage_regex.findall(html)


def get_robots_parser(robots_url):
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp


def link_crawler(start_url, link_regex,
                robots_url=None,
                user_agent='wswp'):
    crawl_queue = [start_url]
    seen =  {}
    if not robots_url:
        robots_url = start_url+'/robots.txt'
    rp = get_robots_parser(robots_url)
    
    while crawl_queue:
        url = crawl_queue.pop()
        # check url pases robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            html = download(url, user_agent=user_agent)
        else:
            print('Blocked by robots.txt...', url)

## to check that it does looks into robots.txt and follows its rules

link_crawler('http://example.webscraping.com',
             '/(view|places)/',
             user_agent='BadCrawler')

get_robots_parser('http://example.webscraping.com/robots.txt')

rp = urllib.robotparser.RobotFileParser()
rp.set_url("http://www.musi-cal.com/robots.txt")
rp.read()



#### using proxies in urllip though there are easier ways

proxy = 'http://myproxy.net:1234' # example proxy
proxy_support = urllib.request.ProxyHandler({'http': proxy})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)
### now request via urllib.request will be handled via proxy

######################################################
# full updated crawler with proxy support, but beware it doesn't 
# support https proxies

import re
import urllib.request
from urllib import robotparser
from urllib.parse import urljoin
from urllib.error import URLError, HTTPError, ContentTooShortError


def download(url, num_retries=2, 
            user_agent='wswp', charset='utf-8',
            proxy=None):
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)

    try:
        if proxy:
            # from this point proxy data is added to urllib.request
            proxy_support = urllib.request.ProxyHandler({'http': proxy})
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)

        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html


def get_links(html):
    """return a list of links from html"""
    # a regex to extract all links from the page
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list of all links from the page
    return webpage_regex.findall(html)


def get_robots_parser(robots_url):
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp


def link_crawler(start_url, link_regex,
                robots_url=None,
                user_agent='wswp',
                proxy=None):
    crawl_queue = [start_url]
    seen =  {}
    if not robots_url:
        robots_url = start_url+'/robots.txt'
    rp = get_robots_parser(robots_url)
    
    while crawl_queue:
        url = crawl_queue.pop()
        # check url pases robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            html = download(url, user_agent=user_agent, proxy=proxy)
        else:
            print('Blocked by robots.txt...', url)

## to check that it does looks into robots.txt and follows its rules

link_crawler('http://example.webscraping.com',
             '/(view|places)/',
             proxy='http://myproxy.net:1234')

#######################################
#######################################
## Throttling downloads

## throttling class


import urllib.request
from urllib import robotparser
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.error import URLError, HTTPError, ContentTooShortError
import time
import re


#### create a class to delay the visit to the same url 

class Throttle:
    """ Add a delay between downloads to the same domain
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (time.time() - last_accessed)
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                time.sleep(sleep_secs)
        # update the last accessed time
        self.domains[domain] = time.time()

#### class over



def download(url, num_retries=2, 
            user_agent='wswp', charset='utf-8',
            proxy=None):
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)

    try:
        if proxy:
            # from this point proxy data is added to urllib.request
            proxy_support = urllib.request.ProxyHandler({'http': proxy})
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)

        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html


def get_links(html):
    """return a list of links from html"""
    # a regex to extract all links from the page
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list of all links from the page
    return webpage_regex.findall(html)


def get_robots_parser(robots_url):
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp




def link_crawler(start_url, link_regex,
                robots_url=None,
                user_agent='wswp',
                proxy=None,
                delay=3):
    crawl_queue = [start_url]
    seen =  set()
    if not robots_url:
        robots_url = start_url+'/robots.txt'
    rp = get_robots_parser(robots_url)
    throttle = Throttle(delay)

    # we add throttle here, but I'm not sure yet why
    
    while crawl_queue:
        url = crawl_queue.pop()
        # check url pases robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)

            html = download(url, user_agent=user_agent, proxy=proxy)
            if not html:
                continue
            # filler for links matching our regex
            for link in get_links(html):
                if re.match(link_regex, link):
                    abs_link = urljoin(start_url, link)
                    if abs_link not in seen:
                        seen.add(abs_link)
                        crawl_queue.append(abs_link)
            
            
            if not html:
                continue
            # TODO: add actual data scraping here

        else:
            print('Blocked by robots.txt...', url)



link_crawler('http://example.webscraping.com',
             '/(view|places)/')
        


#########################################################
#########################################################
### Adding the depth of crawl to avoid spider traps

import urllib.request
from urllib import robotparser
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.error import URLError, HTTPError, ContentTooShortError
import time
import re


#### create a class to delay the visit to the same url 

class Throttle:
    """ Add a delay between downloads to the same domain
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (time.time() - last_accessed)
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                time.sleep(sleep_secs)
        # update the last accessed time
        self.domains[domain] = time.time()

#### class over



def download(url, num_retries=2, 
            user_agent='wswp', charset='utf-8',
            proxy=None):
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)

    try:
        if proxy:
            # from this point proxy data is added to urllib.request
            proxy_support = urllib.request.ProxyHandler({'http': proxy})
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)

        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html


def get_links(html):
    """return a list of links from html"""
    # a regex to extract all links from the page
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list of all links from the page
    return webpage_regex.findall(html)


def get_robots_parser(robots_url):
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp




def link_crawler(start_url, link_regex,
                robots_url=None,
                user_agent='wswp',
                proxy=None,
                delay=3,
                max_depth=4):
    crawl_queue = [start_url]
    seen =  {}
    if not robots_url:
        robots_url = start_url+'/robots.txt'
    rp = get_robots_parser(robots_url)
    throttle = Throttle(delay)

    # we add throttle here, but I'm not sure yet why
    
    while crawl_queue:
        url = crawl_queue.pop()
        # check url pases robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            depth = seen.get(url,0)
            if depth == max_depth:
                print(f'Skipping url... {url} due to depth')
                continue

            throttle.wait(url)

            html = download(url, user_agent=user_agent, proxy=proxy)
            if not html:
                continue
            # filler for links matching our regex
            for link in get_links(html):
                if re.match(link_regex, link):
                    abs_link = urljoin(start_url, link)
                    if abs_link not in seen:
                        seen[abs_link] = depth + 1
                        crawl_queue.append(abs_link)
            
            
            if not html:
                continue
            # TODO: add actual data scraping here

        else:
            print('Blocked by robots.txt...', url)



link_crawler('http://example.webscraping.com',
             '/(view|places)/',
             max_depth=1)


#######################################################################
########### Using request library  ####################################
### the biggest change in the fn download()

import re
from urllib import robotparser
from urllib.parse import urljoin
import requests

#### create a class to delay the visit to the same url 

class Throttle:
    """ Add a delay between downloads to the same domain
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (time.time() - last_accessed)
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                time.sleep(sleep_secs)
        # update the last accessed time
        self.domains[domain] = time.time()

#### class over



def download(url, num_retries=2, 
            user_agent='wswp',
            proxies=None):

    """ Download a given URL and return the page content
        args:
            url (str): URL
        kwargs:
            user_agent (str): user agent (default: wswp)
            proxies (dict): proxy dict w/ keys 'http' and 'https', values
                            are strs (i.e. 'http(s)://IP') (default: None)
            num_retries (int): # of retries if a 5xx error is seen (default: 2)
    """
    print('Downloading:', url)
    headers = {'User-Agent': user_agent, }
    try:
        resp = requests.get(url, headers=headers, proxies=proxies)
        html = resp.text
        if resp.status_code >= 400:
            print('Download error:', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                return download(url, num_retries-1)

    except requests.exceptions.RequestException as e:
        print('Download error:', e.reason)
        html = None

    return html


def get_links(html):
    """return a list of links from html"""
    # a regex to extract all links from the page
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list of all links from the page
    return webpage_regex.findall(html)


def get_robots_parser(robots_url):
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp




def link_crawler(start_url, link_regex,
                robots_url=None,
                user_agent='wswp',
                proxies=None,
                delay=3,
                max_depth=4):
    crawl_queue = [start_url]
    seen =  {}
    if not robots_url:
        robots_url = start_url+'/robots.txt'
    rp = get_robots_parser(robots_url)
    throttle = Throttle(delay)

    # we add throttle here, but I'm not sure yet why
    
    while crawl_queue:
        url = crawl_queue.pop()
        # check url pases robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            depth = seen.get(url,0)
            if depth == max_depth:
                print(f'Skipping url... {url} due to depth')
                continue

            throttle.wait(url)

            html = download(url, user_agent=user_agent, proxies=proxies)
            if not html:
                continue
            # filler for links matching our regex
            for link in get_links(html):
                if re.match(link_regex, link):
                    abs_link = urljoin(start_url, link)
                    if abs_link not in seen:
                        seen[abs_link] = depth + 1
                        crawl_queue.append(abs_link)
            
            
            if not html:
                continue
            # TODO: add actual data scraping here

        else:
            print('Blocked by robots.txt...', url)



link_crawler('http://example.webscraping.com',
             '/(view|places)/',
             max_depth=1)


#########################################################
#########################################################
## Srcaping 

import re

def download(url, num_retries=2, user_agent='wswp', charset='utf-8', proxy=None):

    """ Download a given URL and return the page content
        args:
            url (str): URL
        kwargs:
            user_agent (str): user agent (default: wswp)
            charset (str): charset if website does not include one in headers
            proxy (str): proxy url, ex 'http://IP' (default: None)
            num_retries (int): number of retries if a 5xx error is seen (default: 2)
    """
    print('Downloading:', url)
    request = urllib.request.Request(url)
    request.add_header('User-agent', user_agent)
    try:
        if proxy:
            proxy_support = urllib.request.ProxyHandler({'http': proxy})
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)
        resp = urllib.request.urlopen(request)
        cs = resp.headers.get_content_charset()
        if not cs:
            cs = charset
        html = resp.read().decode(cs)
    except (URLError, HTTPError, ContentTooShortError) as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    return html


url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
html = download(url)
re.findall(r'<td class="w2p_fw">(.*?)</td>', html) # searches for what sits between tags
## <td class="w2p_fw"> .... </td>

### for country area we'd scrape 
re.findall(r'<td class="w2p_fw">(.*?)</td>', html)[1]

###
re.findall(r'<tr id="places_area__row"><td class="w2p_fl"><label class="readonly" for="places_area" id="places_area__label">Area: </label></td><td class="w2p_fw">(.*?)</td>', html)

### things can change like swaping " for ' in a page. Below an improved version

re.findall('''<tr id="places_area__row">.*?<td\s*class=["']w2p_fw["']>(.*?)</td>''', html)


####################################################################
### Beautiful Soup

"""
<ul class=country>
    <li>Area
    <li>Population
</ul>
"""

from bs4 import BeautifulSoup
from pprint import pprint
broken_html = '<ul class=country><li>Area<li>Population</ul>'
# parse the HTML
soup = BeautifulSoup(broken_html, 'html.parser') # not totaly corrects the bad code
fixed_html = soup.prettify()
pprint(fixed_html)
pprint(soup)

### with html5lib
soup = BeautifulSoup(broken_html, 'html5lib') # not totaly corrects the bad code
fixed_html = soup.prettify()
pprint(fixed_html)
pprint(soup)

### and lxml is more or less the same
soup = BeautifulSoup(broken_html, 'lxml') # not totaly corrects the bad code
fixed_html = soup.prettify()
pprint(fixed_html)
pprint(soup)

### now that we have the BS object with repaired and parsed code we can find the elements we need
ul = soup.find('ul', attrs={'class':'country'})
ul.find('li') # returns the 1st match 
ul.find_all('li')


### full code on how to extract a country area from our example website

from bs4 import BeautifulSoup
url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
html = download(url)
soup = BeautifulSoup(html, 'lxml')
# locate the area row
tr = soup.find(attrs={'id':'places_area__row'}) # searching by html attribute id
td = tr.find(attrs={'class':'w2p_fw'}) # locate the cell in the row found above
area = td.text
print(area)


#######################################################################
## Lxml -  it's the fastest from performance point of view - it's written in C
from lxml.html import fromstring, tostring
from pprint import pprint
broken_html = '<ul class=country><li>Area<li>Population</ul>'
tree = fromstring(broken_html) # parse HTML
fixed_html  = tostring(tree, pretty_print=True)
print(fixed_html)


### with CSS  selectors

# import re
# from urllib import robotparser
# from urllib.parse import urljoin

import requests
def download(url, num_retries=2, 
            user_agent='wswp',
            proxies=None):

    """ Download a given URL and return the page content
        args:
            url (str): URL
        kwargs:
            user_agent (str): user agent (default: wswp)
            proxies (dict): proxy dict w/ keys 'http' and 'https', values
                            are strs (i.e. 'http(s)://IP') (default: None)
            num_retries (int): # of retries if a 5xx error is seen (default: 2)
    """
    print('Downloading:', url)
    headers = {'User-Agent': user_agent, }
    try:
        resp = requests.get(url, headers=headers, proxies=proxies)
        html = resp.text
        if resp.status_code >= 400:
            print('Download error:', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                return download(url, num_retries-1)

    except requests.exceptions.RequestException as e:
        print('Download error:', e.reason)
        html = None

    return html


url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
html = download(url)
tree = fromstring(html)
td = tree.cssselect('tr#places_area__row > td.w2p_fw')[0]
area = td.text_content()
print(area)

# typical patterns for CSS selection in tree.cssselect
"""
Select any tag: *
Select by tag <a>: a
Select by class of "link": .link
Select by tag <a> with class "link": a.link
Select by tag <a> with ID "home": a#home
Select by child tag <span> of parent tag <a>: a > span
Select by descendant <span> of tag <a>: a span
Select by tag <a> with attribute title of "Home": a[title=Home] # this one is interesting
"""

# a = tree.cssselect('label[id=places_area__label]')
# a[0].text_content()
# [print(i.text_content()) for i in a]



### make sure I install detectem module and learn how to use it

##############################################################
####### XPath selectors with LXML
"""
Selector description                                        XPath Selector                          CSS selector
Select all links                                            '//a'                                   'a'
Select div with class "main"                                '//div[@class="main"]'                  'div.main'
Select ul with ID "list"                                    '//ul[@id="list"]'                      'ul#list'
Select text from all paragraphs                             '//p/text()'                            'p'*
Select all divs which contain 'test' in the class           '//div[contains(@class, 'test')]'       'div [class*="test"]'
Select all divs with links or lists in them                 '//div[a|ul] '                          'div a, div ul'
Select a link with google.com in the href                   '//a[contains(@href, "google.com")]     'a'*
"""

url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
html = download(url)
tree = fromstring(html)
area = tree.xpath('//tr[@id="places_area__row"]/td[@class="w2p_fw"]/text()')[0]
print(area)

#### I can test the selectors (CSS and XPath) in the browser
#### CSS with $('tr') - example to find a table raws
#### XPath with $x('//td/img')

###################################################################################
#### Travrsing family tree with LXML

url = 'http://example.webscraping.com/places/default/view/United-Kingdom-239'
html = download(url)
tree = fromstring(html)
table = tree.xpath('//table')[0]
table.getchildren()

previous_siblings = table.getprevious()
print(previous_siblings)

next_siblings = table.getnext()
print(next_siblings)

table.getparent()


##########################################################
## Comparing performance
import re
from bs4 import BeautifulSoup
from lxml.html import fromstring
import requests

####
def download(url, num_retries=2, 
            user_agent='wswp',
            proxies=None):

    """ Download a given URL and return the page content
        args:
            url (str): URL
        kwargs:
            user_agent (str): user agent (default: wswp)
            proxies (dict): proxy dict w/ keys 'http' and 'https', values
                            are strs (i.e. 'http(s)://IP') (default: None)
            num_retries (int): # of retries if a 5xx error is seen (default: 2)
    """
    print('Downloading:', url)
    headers = {'User-Agent': user_agent, }
    try:
        resp = requests.get(url, headers=headers, proxies=proxies)
        html = resp.text
        if resp.status_code >= 400:
            print('Download error:', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                return download(url, num_retries-1)

    except requests.exceptions.RequestException as e:
        print('Download error:', e.reason)
        html = None

    return html

#####
### these are names in the id of each row 'tr'
FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent',
'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format',
'postal_code_regex', 'languages', 'neighbours')

def re_scraper(html):
    """ Using regex to extract data from country pages. """
    results = {}
    for field in FIELDS:
        results[field] = re.search(f'<tr id="places_{field}__row">.*?<td class="w2p_fw">(.*?)</td>', html).groups()[0]
    return results



def bs_scraper(html):
    """ Using BeautifulSoup to extract data from country pages."""
    soup = BeautifulSoup(html, 'html5lib')
    results = {}
    for field in FIELDS:
        results[field] = soup.find('table').find('tr', id=f'places_{field}__row').find('td', class_='w2p_fw').text

    return results




def lxml_srcaper(html):
    """ Using lxml and cssselect to extract data from country pages. """
    tree = fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.cssselect(f'table > tr#places_{field}__row > td.w2p_fw')[0].text_content()

    return results




def lxml_xpath_scraper(html):
    """ Using lxml and xpath to extract data from country pages. """
    tree = fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.xpath(f'//tr[@id="places_{field}__row"]/td[@class="w2p_fw"]')[0].text_content()

    return results


#### compare all the different types
import time

NUM_ITERATIONS = 1000 # number of times to test each scraper
html = download('http://example.webscraping.com/places/default/view/United-Kingdom-239')

scrapers = [
    ('Regular Expressions', re_scraper),
    ('BeautifulSoup', bs_scraper),
    ('Lxml', lxml_srcaper),
    ('Xpath', lxml_xpath_scraper),]


for name, scraper in scrapers:
    # record start time of scrape
    start = time.time()
    for i in range(NUM_ITERATIONS):
        if scraper == re_scraper:
            re.purge()
        result = scraper(html)
        # check scraped tesult is as expected
        assert result['area'] == '244,820 square kilometres'
    # recors end time of the srcape and output the total
    end = time.time()
    print(f'{name}...{end - start:.2f} seconds')


######### Results ##########
## Regular Expressions...1.65 seconds
## BeautifulSoup...7.20 seconds  # with 'lxml'
## BeautifulSoup...7.30 seconds  # with 'html.parser'
## BeautifulSoup...7.30 seconds  # with 'html5lib'
## Lxml with CSS ...2.12 seconds
## Lxml with Xpath...0.97 seconds - winner!!



