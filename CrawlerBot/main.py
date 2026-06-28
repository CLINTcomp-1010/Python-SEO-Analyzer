import threading
from queue import Queue
from CrawlerBot.spider import Spider
from CrawlerBot.domain import *
from CrawlerBot.general import *

NUMBER_OF_THREADS = 8
queue = Queue()

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs(queue_file):
    for link in file_to_set(queue_file):
        queue.put(link)
    queue.join()
    crawl(queue_file)


# Check if there are items in the queue, if so crawl them
def crawl(queue_file):
    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs(queue_file)
