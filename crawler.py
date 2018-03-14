import urllib.request
from bs4 import BeautifulSoup
import queue
import threading
import sys


class Crawler:
    visited = set()
    url_queue = queue.Queue()

    # Start off with adding the main url in the queue
    # and creating our threadpool. We then start processing
    # the queue
    def __init__(self):
        print("Starting...")
        url = self.get_root_url(sys.argv)
        self.url_queue.put(url)
        self.create_threadpool()
        self.url_queue.join()

    # Check if any CLI arguments are given, and if so take that
    # as root url
    def get_root_url(self, args):
        if len(args) == 1:
            return "http://www.rescale.com"
        else:
            return args[1]

    # Get the latest url in queue and visit it
    def process_request(self):
        while True:
            url = self.url_queue.get()
            self.crawl(url)
            self.url_queue.task_done()

    # Creates the threads to execute requests
    def create_threadpool(self):
        for _ in range(8):
            t = threading.Thread(target=self.process_request)
            t.daemon = True
            t.start()

    # Add to visited, get links in the url and process it
    def crawl(self, url):
        self.visited.add(url)
        links = self.get_links(url)
        self.process_result(url, links)

    # Print the result of the url and links
    def process_result(self, url, links):
        print(url)
        for link in links:
            url = link.get("href")
            # Filter out only the absolute links
            if str(url).startswith("http"):
                if url not in self.visited:
                    print("\t" + url)
                    self.url_queue.put(url)

    # Make HTTP request and convert to BeautifulSoup
    # document to get list of <a href>
    def get_links(self, url):
        body = BeautifulSoup(self.get_body(url), "html.parser")
        return body.findAll("a")

    # Make actual HTTP request
    def get_body(self, url):
        response = urllib.request.urlopen(url)
        html = response.read()
        return html


crawler = Crawler()
