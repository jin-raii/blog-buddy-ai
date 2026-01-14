import os 
from crewai import Agent, Crew, Process, Task, LLM
import asyncio
from langchain_ollama import ChatOllama

async def main():
    # llm = LLM(model="ollama/olmo-3:7b", temperature=0.7, max_tokens=512, base_url="http://localhost:11434")
    llm = ChatOllama(model="olmo-3:7b", base_url="http://localhost:11434", temperature=0.7, max_tokens=512)
    # response = await llm.acall('what is the capital of Nepal?')
    prompt = "what is the capital of Nepal?"
    # print(response.text)
    message = [
        ('system', 'You are a helpful assistant.'),
        ('user', prompt)
    ]
    response = llm.invoke(message)
    stream = llm.stream(response.content)
    full = next(stream)
    for chunk in stream:
        full += chunk
    print(full, end='', flush=True)


if __name__ == "__main__":
    asyncio.run(main())
