import asyncio
import aiohttp

import requests
import json

import requests


API_URL = "http://localhost:8000/"
proxies = {
    "http": None,
    "https": None,
}
proxy = ""

async def test_example_1():
    print(1)
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, proxy=proxy) as response:
            result = await response.text()
            print(result)


async def test_example_2():
    print(2)
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, proxy=proxy) as response:
            result = await response.text()
            print(result)


async def main():
    await asyncio.gather(test_example_1(), test_example_2())


if __name__ == "__main__":
    asyncio.run(main())
