import aiohttp

class JikanHandler():
    def __init__(self):
        self.base_url = "https://api.jikan.moe/v4"

    async def fetch_random_anime(self, session: aiohttp.ClientSession, params: dict = None):
        if params:
            query_string = "&".join(f"{key}={value}" for key, value in params.items())
            full_url = f"{self.base_url}/anime?{query_string}&limit=25"  # Fetch up to 25 results
        else:
            full_url = f"{self.base_url}/random/anime"

        async with session.get(full_url) as response:
            if response.status != 200:
                return None
            data = await response.json()
        return data
    async def fetch_random_manga(self, session: aiohttp.ClientSession, params: dict = None):
        if params:
            query_string = "&".join(f"{key}={value}" for key, value in params.items())
            full_url = f"{self.base_url}/manga?{query_string}&limit=25"  # Fetch up to 25 results
        else:
            full_url = f"{self.base_url}/random/manga"

        async with session.get(full_url) as response:
            if response.status != 200:
                return None
            data = await response.json()
        return data
