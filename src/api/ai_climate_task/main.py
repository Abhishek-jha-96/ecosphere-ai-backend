from argparse import ArgumentParser
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
        self.prompt = ""

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
        self.cleaned_data = [item.strip() for item in self.ai_context_data if item]

    def _populate_prompt(self):
        self.prompt = (
            f"Summarize climate impact for {self.location}: {self.cleaned_data}"
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
            self._clean_context_data()
            self._populate_prompt()
            self._llm_call()
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
