from queue import Queue

from statsf1.models.core import DownloadThread
from statsf1.tools.logger import log_races


class Downloader:
    def __init__(self, races, db, n_threads=8):
        self.races = races
        self.n_threads = n_threads
        self.db = db

    def run(self):
        log_races(self.races)

        queue = Queue()
        for race in self.races:
            queue.put(race)

        for i in range(self.n_threads):
            t = DownloadThread(queue, self.db)
            t.start()

        queue.join()
