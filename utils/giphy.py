from urllib import parse
import aiohttp
import json
import os
import asyncio

if "REPLIT" in os.environ:
    api_key = os.environ["giphy_api_key"]
else:
    with open("config.json", "r") as file:
        api_key = json.load(file)["giphy_api_key"]

endpoint = "http://api.giphy.com/v1/gifs/search"

async def search(query: str, limit: int = 5) -> dict:
    params = parse.urlencode({
      "q": query,
      "api_key": api_key,
      "limit": limit
})
    url = endpoint + "?" + params
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = json.loads(await response.content.read())
            
            
        return data
        

    
    