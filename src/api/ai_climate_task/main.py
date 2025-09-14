from argparse import ArgumentParser

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.api.ai_climate_task.prompt import CLIMATE_TASK_PROMPT
from src.core.db import get_db
from .settings import IN_PROGRESS, COMPLETED, FAILED
from .serp_api_client import SerpApiClient


class AIClimateTask:
    def __init__(self):
        self.location = ""
        self.query = ""
        self.task_id = None
        self.task_status = IN_PROGRESS

        self.ai_context_data = {}
        self.cleaned_data = {}
        self.clustered_data = None
        self.structured_context = None
        self.prompt = ""

        self.db = get_db()

        self.serp_api_client = SerpApiClient()
        self.parse_args()

    def parse_args(self):
        parser = ArgumentParser()
        parser.add_argument("--location", type=str, required=True)
        parser.add_argument("--query", type=str, required=True)
        parser.add_argument("--task_id", type=str, required=True)

        args = parser.parse_args()
        self.location = args.location
        self.query = args.query
        self.task_id = args.task_id

    def _clean_context_data(self):
        """
        Step 1. Deduplicate news data
        """
        seen = set()
        cleaned = []
        for item in self.ai_context_data:
            snippet = item.get("snippet", "").strip()
            if snippet and snippet not in seen:
                cleaned.append(item)
                seen.add(snippet)
        self.cleaned_data = cleaned

    def _summarize_articles(self):
        """
        Step 2. Summarize each article
        """
        summaries = []
        for item in self.cleaned_data:
            snippet = item.get("snippet", "")
            # take up to 2 sentences
            parts = snippet.split(". ")
            summary = ". ".join(parts[:2]).strip()
            summaries.append(
                {
                    "topic": item.get("title", "Untitled"),
                    "summary": summary,
                    "source": item.get("link", ""),
                    "date": item.get("date", ""),
                }
            )
        self.cleaned_data = summaries

    def _cluster_articles(self, threshold: float = 0.4):
        """
        Step 3. Thematic clustering using TF-IDF + cosine similarity
        """
        texts = [item["summary"] for item in self.cleaned_data]
        if not texts:
            self.clustered_data = []
            return

        vectorizer = TfidfVectorizer(stop_words="english")
        X = vectorizer.fit_transform(texts)
        sim_matrix = cosine_similarity(X)

        clusters = []
        used = set()
        for i in range(len(texts)):
            if i in used:
                continue
            cluster = [i]
            used.add(i)
            for j in range(i + 1, len(texts)):
                if j not in used and sim_matrix[i, j] >= threshold:
                    cluster.append(j)
                    used.add(j)
            clusters.append(cluster)

        grouped = []
        for cluster in clusters:
            grouped.append(
                {
                    "theme": self.cleaned_data[cluster[0]]["topic"],
                    "articles": [self.cleaned_data[idx] for idx in cluster],
                }
            )
        self.clustered_data = grouped

    def _generate_structured_context(self):
        """
        Step 4. Generate structured JSON-like context for LLM
        """
        structured = {"location": self.location, "query": self.query, "themes": []}

        for group in self.clustered_data:
            structured["themes"].append(
                {
                    "topic": group["theme"],
                    "summary": " | ".join([a["summary"] for a in group["articles"]]),
                    "sources": [a["source"] for a in group["articles"]],
                    "dates": [a["date"] for a in group["articles"]],
                }
            )

        self.structured_context = structured

    def _populate_prompt(self):
        self.prompt = CLIMATE_TASK_PROMPT.format(
            location=self.location,
            query=self.query,
            theme_topic=self.structured_context["themes"][0]["topic"],
            theme_summary=self.structured_context["themes"][0]["summary"],
            theme_sources=", ".join(self.structured_context["themes"][0]["sources"]),
            theme_dates=", ".join(self.structured_context["themes"][0]["dates"]),
        )

    def _llm_call(self):
        self.llm_output = (
            f"LLM summary for {self.location} based on query '{self.query}'."
        )

    def _update_db(self):
        print(f"Updating DB for task {self.task_id} with status {self.task_status}")

    def create_task(self):
        try:
            print("AI Climate Task creation script started.")
            self.ai_context_data = self.serp_api_client.search_news(
                query=self.query, location=self.location
            )
            # Data preparation pipeline
            self._clean_context_data()
            self._summarize_articles()
            self._cluster_articles()
            self._generate_structured_context()

            # Generate prompt
            self._populate_prompt()

            # LLM call
            self._llm_call()

            # Update record and save response
            self._update_db()
            self.task_status = COMPLETED

            print("AI Climate Task creation script completed.")
        except Exception as e:
            self.task_status = FAILED
            print(f"Error creating AI Climate Task: {e}")

    def update_task_status(self):
        print(f"Task {self.task_id} finished with status: {self.task_status}")


if __name__ == "__main__":
    ai_climate_task = AIClimateTask()
    ai_climate_task.create_task()
    ai_climate_task.update_task_status()
