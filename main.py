import os 
from crewai import Agent, Crew, Process, Task, LLM
import asyncio
from langchain_ollama import ChatOllama
from crewai_tools import FirecrawlScrapeWebsiteTool 
from dotenv import load_dotenv

load_dotenv()


# llm = LLM(model="ollama/olmo-3:7b", temperature=0.7, max_tokens=512, base_url="http://localhost:11434")
llm = ChatOllama(model="olmo-3:7b", base_url="http://localhost:11434", temperature=0.7, max_tokens=512)
# response = await llm.acall('what is the capital of Nepal?')
# prompt = "what is the capital of Nepal?"
# # print(response.text)
# message = [
#     ('system', 'You are a helpful assistant.'),
#     ('user', prompt)
# ]
# response = llm.invoke(message)
# stream = llm.stream(response.content)
# full = next(stream)
# for chunk in stream:
#     full += chunk
# print(full, end='', flush=True)

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
    Verbose=True, 
    allow_delegation=False

)



agent_summarizer = Agent(
    name="Summarizer Agent",
    role="A summarization agent that summarizes text content.",
    goal="Summarize the extracted content into concise summaries.",
    backstory="You are an expert summarizer.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# define task 

def scrape_task(url: str, agent: Agent):
    return Task(
        description=(f"Scrape the website at {url} using FirecrawlScrapeWebsiteTool."
                    "Extract the main content, headings, and any relevant metadata. filtering out ads and navigation elements."),
        expected_output="Extracted content from the website.",
        agent=agent,
    ) 

def summarize_task(content: str, agent: Agent):
    return Task(
        description=(f"Summarize the extracted content.{content}."
                    "Provide a concise summary highlighting the key points and main ideas."),
        expected_output=("A concise summary of the content."
                        "Ensure the summary is clear and captures the essence of the original text."),
        agent=agent,
        context=[content]
    )

# create a crew with the agents
def crew_process(url: str, scrape_agent: Agent, summarizer_agent: Agent):
    scrape_task = scrape_task(url, scrape_agent)
    summarize_task = summarize_task(scrape_task, summarizer_agent)

    crew = Crew(
        agents=[scrape_agent, summarizer_agent],
        tasks=[scrape_task, summarize_task],
        verbose=True,
        process=Process.SEQUENTIAL
    )

    return crew 




if __name__ == "__main__":
    url = 'https://ekantipur.com/'
    crew = crew_process(url, scrape_agent, agent_summarizer)
     # run the crew
    asyncio.run(crew.kickoff())
