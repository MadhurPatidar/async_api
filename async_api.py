import asyncio
import aiohttp
import async_timeout
import json

async def fetch_data(url, session):
    try:
        async with async_timeout.timeout(10):  # Timeout set to 10 seconds
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"Failed to fetch data from {url}, status {response.status}"}
    except asyncio.TimeoutError:
        return {"error": f"Timeout error while fetching data from {url}"}
    except aiohttp.ClientError as e:
        return {"error": f"Aiohttp client error: {str(e)}"}

async def fetch_from_multiple_apis(api_urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in api_urls:
            task = asyncio.create_task(fetch_data(url, session))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

# Example usage:
async def main():
    api_urls = [
        'https://api.example.com/data1',
        'https://api.example.com/data2',
        'https://api.example.com/data3'
    ]
    results = await fetch_from_multiple_apis(api_urls)
    print(json.dumps(results, indent=2))

# To run the asyncio event loop (for testing purposes):
if __name__ == '__main__':
    asyncio.run(main())
