from serpapi import GoogleSearch
from .settings import SERP_API_KEY


class SerpApiClient:
    def __init__(self, location: str = "India,New Delhi"):
        self.api_key = SERP_API_KEY
        self.location = location

    def search(self, query: str, **kwargs) -> dict:
        """Generic search using SerpAPI."""
        params = {
            "q": query,
            "location": self.location,
            "api_key": self.api_key,
            **kwargs,
        }
        search = GoogleSearch(params)
        return search.get_dict()

    def search_news(
        self, query: str, timeframe: str = "d", num: int = 10
    ) -> list[dict]:
        """
        Search Google News for a query.
        :param query: search keyword(s)
        :param timeframe: 'h' (last hour), 'd' (last 24h), 'w' (last week), etc.
        :param num: number of results to fetch
        :return: list of news results
        """
        result = self.search(
            query,
            tbm="nws",  # Google News
            tbs=f"qdr:{timeframe}",
            num=num,
        )
        return result.get("news_results", [])
