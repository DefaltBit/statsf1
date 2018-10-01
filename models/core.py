#!/usr/bin/env python3
# coding: utf-8


""" Download models used across app """

import threading


class DownloadThread(threading.Thread):
    def __init__(self, queue, local_db):
        super(DownloadThread, self).__init__()
        self.queue = queue
        self.local_db = local_db
        self.daemon = True

    def run(self):
        while True:
            try:
                url = self.queue.get()
                # todo save to db
            except Exception as e:
                print(e)

            self.queue.task_done()
