import atexit
import logging

from search.crawler import Crawler
from search.frontier import Frontier

class Crawl:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s (%(name)s) %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO)
        self.frontier = Frontier()
        self.frontier.load_frontier()
        atexit.register(self.frontier.save_frontier)
        self.crawler = Crawler(self.frontier)
        self.crawler.start_crawling()
    



