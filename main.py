import os 
from crewai import Agent, Crew, Process, Task, LLM
import asyncio

from crewai_tools import FirecrawlScrapeWebsiteTool 
from dotenv import load_dotenv


load_dotenv()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral:latest")
llm = LLM(model=f"ollama/{OLLAMA_MODEL}", temperature=0.7, base_url=OLLAMA_URL)

tools = [
    FirecrawlScrapeWebsiteTool(
        api_key=os.getenv("FIRECRAWL_ENV"),
    )
]


# create an agent with the LLM and tools
scrape_agent = Agent(
    name="ScrapeAgent",
    role="A web scraping agent that uses Firecrawl to scrape websites.",
    goal="Extract relevant information from websites using Firecrawl.",
    backstory="You are an expert web scraper with access to Firecrawl.",
    llm=llm,
    tools=tools,
    verbose=True, 
    allow_delegation=False,
    use_system_prompt=False  # Disable to avoid LLM compatibility issues
)



agent_summarizer = Agent(
    name="Summarizer Agent",
    role="A summarization agent that summarizes text content.",
    goal="Summarize the extracted content into concise summaries.",
    backstory="You are an expert summarizer.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
    use_system_prompt=False  
)

# define task 

def scrape_task(url: str, agent: Agent):
    return Task(
        description=(
            f"Scrape the website at {url} using FirecrawlScrapeWebsiteTool. "
            "Extract only the main readable content of the page. "
            "Include all meaningful headings (H1–H6) and relevant metadata such as "
            "page title, meta description, author (if available), publish date, and canonical URL. "
            "Exclude advertisements, navigation menus, footers, sidebars, pop-ups, and any non-content elements."
        ),
        expected_output=(
            "A structured object containing:\n"
            "- main_content: cleaned article or page text\n"
            "- headings: a list of headings in order\n"
            "- metadata: title, description, author, publish_date, canonical_url"
        ),
        agent=agent,
    )


def summarize_task(content: str, agent: Agent):
    return Task(
        description=(
            "Summarize the provided content into a concise, well-structured summary. "
            "Focus on the key ideas, main arguments, and essential information. "
            "Avoid unnecessary details and repetition."
        ),
        expected_output=(
            "A clear and concise summary capturing the core ideas of the content "
            "in plain, readable language."
        ),
        agent=agent,
        context=[content],
    )

# create a crew with the agents
def crew_process(url: str, scrape_agent: Agent, summarizer_agent: Agent):
    scrape_task_ = scrape_task(url, scrape_agent)
    summarize_task_ = summarize_task(scrape_task_, summarizer_agent)

    crew = Crew(
        agents=[scrape_agent, summarizer_agent],
        tasks=[scrape_task_, summarize_task_],
        verbose=True,
        process=Process.sequential
    )

    return crew 


def summarize_content(url:str):
    crew = crew_process(url, scrape_agent, agent_summarizer)
    res = crew.kickoff()
    return res.raw

# if __name__ == "__main__":
#     url = ['https://ekantipur.com/', 'https://sebastianraschka.com/llms-from-scratch/']
#     summary = summarize_content(url)
#     print("Final Summary:", summary)
     
