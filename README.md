# Blog Summarizer

Local AI-powered tool that scrapes blog posts and articles from websites, summarizes their content, and optionally converts the summaries to audio using text-to-speech technology.

## Features

- **Web Scraping**: Uses Firecrawl to extract content from websites
- **AI Summarization**: Leverages CrewAI agents with Ollama/Mistral for intelligent content summarization
- **Web Interface**: Clean Gradio-based UI for easy interaction
- **Text-to-Speech**: Generate audio versions of summaries using Pocket TTS


## Prerequisites

- Python 3.12 or higher
- Ollama running locally
- Firecrawl API key

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd summurize-blog
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using uv:
```bash
uv pip install -r requirements.txt
```

## Configuration

1. **Ollama Setup**:
   - Install Ollama from [ollama.ai](https://ollama.ai)
   - Pull the Mistral model:
   ```bash
   ollama pull mistral
   ```
   - Ensure Ollama is running on `http://localhost:11434` (default)

2. **Environment Variables**:
   Create a `.env` file in the project root with:
   ```
   OLLAMA_URL=http://localhost:11434
   FIRECRAWL_ENV=your_firecrawl_api_key_here
   ```

## Usage

### Web Interface (Recommended)

Run the Gradio web application:

```bash
python app.py
```

This will launch a web interface where you can:
- Enter blog URLs (comma-separated for multiple URLs)
- Click "Summarize" to generate summaries
- Click "Generate Audio" to convert summaries to speech

### Command Line

You can also use the summarization functionality programmatically:

```python
from main import summarize_content

# Summarize a single URL
summary = summarize_content("https://example-blog.com/post")
print(summary)

# Summarize multiple URLs
urls = "https://blog2.com"
summary = summarize_content(urls)
print(summary)
```

## Project Structure

```
summurize-blog/
├── app.py              # Gradio web interface
├── main.py             # Core summarization logic with CrewAI agents
├── pyproject.toml      # Project configuration
├── requirements.txt    # Python dependencies

```

## Dependencies

- **crewai**: Multi-agent AI framework
- **firecrawl-py**: Web scraping tool
- **gradio**: Web UI framework
- **pocket-tts**: Text-to-speech conversion
- **langchain-ollama**: Ollama integration for LangChain
- **python-dotenv**: Environment variable management

## How It Works

1. **Scraping Agent**: Uses Firecrawl to extract clean content from web pages, filtering out ads and navigation
2. **Summarization Agent**: Processes the extracted content using AI to create concise, meaningful summaries
3. **Audio Generation**: Optional text-to-speech conversion using Pocket TTS with voice cloning

## API Keys Required

- **Firecrawl API Key**: Sign up at [firecrawl.dev](https://firecrawl.dev) for web scraping capabilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request


## Troubleshooting

- **Ollama Connection Issues**: Ensure Ollama is running and accessible at the configured URL
- **Firecrawl Errors**: Verify your API key is valid and has sufficient credits
- **Audio Generation Failures**: Check that Pocket TTS dependencies are properly installed

## Future Enhancements

- Support for additional LLM providers
- Batch processing capabilities
- Export summaries to various formats (PDF, DOCX)
- Integration with more TTS engines
- API endpoints for programmatic access
- Process multiple blog URLs simultaneously