import os 
from crewai import Agent, Crew, Process, Task, LLM
import asyncio

async def main():
    llm = LLM(model="ollama/olmo-3:7b", temperature=0.7, max_tokens=512, streaming=True, base_url="http://localhost:11434")
    response = await llm.acall('what is the capital of Nepal?')
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
