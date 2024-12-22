import json
from scrapegraphai.graphs import SmartScraperGraph
import os
# OPENAI_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

# Update your graph config
graph_config = {
    "llm": {
        "api_key": OPENROUTER_API_KEY,
        "model": "anthropic/claude-3-sonnet-20240229",
        "api_base": "https://openrouter.ai/api/v1",
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",  # Specifies the embedding model to use
        "temperature": 0,                    # Keeps the generation deterministic
        "base_url": "http://localhost:11434", # Base URL for the embeddings model server
        "batch_size": 32,                    # Number of texts to embed in each batch
        "batch_timeout": 5,                  # Timeout in seconds for batch processing
        "batch_concurrent": True,            # Enable concurrent batch processing
    },
    "verbose": True,
    "headless": False,
}


baseUrl = "https://ai16z.github.io/eliza/docs/"
# List of URLs to scrape
urls = [
    "quickstart/",
    "core/characterfile/",
]

# Process each URL
for url in urls:
    # Create the SmartScraperGraph instance for this URL
    smart_scraper_graph = SmartScraperGraph(
        prompt="Extract me all the documentation from to create a knowlege base",
        source= baseUrl + url,
        config=graph_config
    )

    # Run the pipeline
    try:
        result = smart_scraper_graph.run()
        # Ensure the result exists and is not empty
        if result:
            try:
                # Use URL as part of filename to keep results separate
                filename = f'scraping_output_{url.replace("https://", "").replace("/", "_")}.json'
                with open(filename, 'w') as f:
                    json.dump(result, f, indent=4)
                print(f"Results for {url} successfully saved to {filename}")
            except IOError as e:
                print(f"Error writing to file for {url}: {e}")
        else:
            print(f"No results were returned from the scraper for {url}")

        # Print results to console
        print(f"\nScraping Results for {url}:")
        print(json.dumps(result, indent=4))

    except Exception as e:
        print(f"Error during scraping {url}: {e}")
