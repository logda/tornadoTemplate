import asyncio
import aiohttp

import requests
import json

import requests


API_URL = "http://localhost:9313/example"
proxies = {
    "http": None,
    "https": None,
}
proxy = ""


async def test_example_1():
    payload = {
        "one": 1
    }
    json_data = json.dumps(payload)
    print('post1')
    
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, data=json_data, proxy=proxy) as response:
            result = await response.json()
            print(result)
    


async def test_example_2():
    payload = {"two": 2}
    json_data = json.dumps(payload)
    print('post2')
    
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, data=json_data, proxy=proxy) as response:
            result = await response.json()
            print(result)
    


async def main():
    await asyncio.gather(test_example_1(), test_example_2())


if __name__ == "__main__":
    asyncio.run(main())
