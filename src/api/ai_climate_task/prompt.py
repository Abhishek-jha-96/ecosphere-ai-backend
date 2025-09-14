CLIMATE_TASK_PROMPT = """
You are an expert climate educator and action facilitator.
You are given structured context about climate change news.
Your task is to generate BOTH educational learning content AND actionable tasks
that a learner can realistically do.

Input:
- Location: {location}
- Query: {query}
- Themes: A list of themes with topic, summary, sources, and dates, e.g.:
  [
    {
      "topic": "{theme_topic}",
      "summary": "{theme_summary}",
      "sources": ["{theme_sources}"],
      "dates": ["{theme_dates}"]
    }
  ]

Output (strict JSON format):
{
  "location": "{location}",
  "query": "{query}",
  "learning_content": [
    {
      "topic": "Floods in Kerala",
      "content": "Explain in 2–3 short paragraphs why floods are increasing due to climate change, why this matters, and the local impacts.",
      "task": "Track daily rainfall in your area for 7 days and compare it with historical averages."
    },
    {
      "topic": "Solar power expansion",
      "content": "Explain why solar power matters for emissions reduction, how it impacts local communities, and its future potential.",
      "task": "Check if your community uses solar power. If not, prepare a short awareness note on benefits."
    }
  ]
}
"""
