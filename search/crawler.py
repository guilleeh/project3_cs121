import os
import logging
import re
from urllib.parse import urlparse, urljoin
from search.corpus import Corpus
from lxml import etree, html      #to parse 
from io import StringIO, BytesIO  #to parse from files
from collections import defaultdict

logger = logging.getLogger(__name__)

class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier):
        self.frontier = frontier
        self.corpus = Corpus()

        self.most_valid_links = ["", 0]
        self.subdomain_count = defaultdict(int)
        self.downloaded_urls = []
        self.traps = []

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            # logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            url_data = self.fetch_url(url)

            valid_links = 0  # number of valid links initialized to zero
            for next_link in self.extract_next_links(url_data):
                if self.corpus.get_file_name(next_link) is not None:
                    if self.is_valid(next_link):
                        valid_links += 1
                        self.frontier.add_url(next_link)

            if (valid_links > self.most_valid_links[1]):
                self.most_valid_links[0] = url
                self.most_valid_links[1] = valid_links

        self.write_summary()


    def write_summary (self):
        f = open("analytics.txt", "w+")
        summary = "Subdomains visited:\n"
        #www.ics.uci.edu
        for e in self.subdomain_count:
            summary += "{}: {}\n".format(e, self.subdomain_count[e])
        summary += "\nMost valid out links: \n"
        if self.most_valid_links[0] != "":
            summary += ("{}: {}\n".format(self.most_valid_links[0], self.most_valid_links[1]))
        summary += "\nDownloaded URLs:\n"
        for e in self.downloaded_urls:
            summary += e + "\n"
        summary += "\nTraps:\n"
        for e in self.traps:
            summary += e + "\n"
        
        total = 0

        for e in self.subdomain_count:
            total += self.subdomain_count[e]
        f.write(summary)
        f.close()


    def fetch_url(self, url):
        """
        This method, using the given url, should find the corresponding file in the corpus and return a dictionary
        containing the url, content of the file in binary format and the content size in bytes
        :param url: the url to be fetched
        :return: a dictionary containing the url, content and the size of the content. If the url does not
        exist in the corpus, a dictionary with content set to None and size set to 0 can be returned.
        """        
        url_data = {
            "url": url,
            "content": None,
            "size": 0
        }

        """ get_file_name(url) from corpus file
        Given a url, this method looks up for a local file in the corpus and, if existed, returns the file address. Otherwise
        returns None
        """
        filename = self.corpus.get_file_name(url)

        if (filename != None):
            # str.encode(), which returns a bytes representation of the Unicode string, encoded in the requested encoding.
            url_data["content"] = str.encode(self.read_file(filename))
            # get file's size and store in url_data["size"]
            url_data["size"] = os.path.getsize(filename)
            parsed = urlparse(url)
            scheme = "%s://" % parsed.scheme
            self.downloaded_urls.append(parsed.geturl().replace(scheme, '', 1)) # add the fetched url to downloaded_urls used for analatic
            
            
        return url_data #a dictionary containing the url, content and the size of the content

    def read_file(self, file):
        """
        Given a filename, returns content of file
        """
        file = open(file, "r", encoding="utf8", errors='ignore')
        fileContents = file.read()
        file.close()
        return fileContents

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        """
        outputLinks = []
        if (url_data["size"] == 0):
            return outputLinks
        # from here
        # need to add -> from urlparse import urlparse 

        parsed_current_url = urlparse(url_data['url'])
        #keep count of the subdomains visited
        self.subdomain_count[parsed_current_url.hostname] += 1

        # parsing the html
        # parse : To read from a file or file-like object, which returns an ElementTree object
        
        tree = html.parse(BytesIO(url_data["content"]))
        #e is a dictionary with key as href and url as its value
        for e in tree.xpath('//a'):
            if ('href' in e.attrib):
                url = e.attrib['href'] #We take everything after href, which is the link to a url
                #The urlparse module defines the following functions:
                    #urlparse.urlparse(urlstring[, scheme[, allow_fragments]])
                    #general structure of a URL: scheme://netloc/path;parameters?query#fragment
                parsed_url = urlparse(url)
                # if the statement is for identifying relative url, then would add current url to it to
                # make the relative url absolute url
                # example: .netloc -> "www.google.com"
                if (parsed_url.netloc == ''):
                    # add scheme and .netloc to our path

                    url = urljoin(url_data["url"], url) 
                    #Get base url and possible relative url,
                    #forms absolute url
                    '''
                    URL_DATA    https://www.ics.uci.edu/computing/services/snapshot.php
                    PARSED URL  /computing/account/
                    FINISHED URL   https://www.ics.uci.edu/computing/account/
                    '''
                    # url = url_data["url"] + url
                
                outputLinks.append(url)

        return outputLinks

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """
        parsed = urlparse(url)
        
        #Regex to check if url is valid, contains http or https. source: https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
        if not re.match(r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)", url):
            return False

        #Filter out any repeating directories
        if re.match(r"^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", url):
            self.traps.append(url)
            return False

        #Filter out any urls with calendar
        if re.match("^(calendar+)*(.+day|.+month|.+year|.+Date).*$", url):
            self.traps.append(url)
            return False


        #Filter out any links that require you to log in
        if re.match("^(.+)(sectok+)(.+)*$", url):
            self.traps.append(url)
            return False

        # Filter out any links that have sidebyside in them
        if re.match("^(.+)(sidebyside+)(.+)*$", url):
            self.traps.append(url)
            return False


        try:
            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv| " \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

        except TypeError:
            print("TypeError for ", parsed)
            return False
