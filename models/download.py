#!/usr/bin/env python3
# coding: utf-8


""" Creates local database and downloads data """

import asyncio
import time
import traceback

import aiohttp
from aiosocks.connector import ProxyConnector, ProxyClientRequest
from pymongo import MongoClient

DATABASE_NAME = "statsf1"  # name of mongodb database to use
MONGODB_CLIENT = MongoClient()  # mongodb client
MONGODB_CLIENT.drop_database(DATABASE_NAME)  # remove all previous data
DATABASE = MONGODB_CLIENT[
    DATABASE_NAME
]  # database to use
for coll in DATABASE.collection_names():
    DATABASE[coll].create_index("num", unique=True)  # set primary key


async def fetch_and_save(url, max_attempts=8, sleep_seconds=1):
    for _ in range(max_attempts):
        try:
            conn = ProxyConnector(remote_resolve=True)
            async with aiohttp.ClientSession(
                    connector=conn,
                    request_class=ProxyClientRequest
            ) as session:
                async with session.get(
                        url,
                        proxy="socks5://127.0.0.1:9150"  # tor proxy
                ) as response:  # use tor
                    body = await response.text(encoding='latin-1')
                    result = {
                        "url": str(url),
                        "html": str(body)
                    }  # add url and page source
                    # todo parse result
                    return True  # or false
        except Exception as e:
            time.sleep(sleep_seconds)
            traceback.print_exc()
            print("Cannot get url " + str(url))
            print(str(e))

    return False


async def bound_fetch(sem, url):
    async with sem:
        await fetch_and_save(url, max_attempts=1, sleep_seconds=0)


async def fetch_urls(list_of_urls, max_concurrent=200):
    tasks = []
    sem = asyncio.Semaphore(max_concurrent)

    for url in list_of_urls:
        task = asyncio.ensure_future(bound_fetch(sem, url))
        tasks.append(task)

    responses = asyncio.gather(*tasks)
    await responses


def download(root, local_db):
    pass
    # todo
    # find years
    #  for each year:
    #    find races
    #      for each race:
    #        download data
    #        save data to local db
    # pro: 1 async for each race
