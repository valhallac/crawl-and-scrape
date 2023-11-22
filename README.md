# Web Scraping Tool

## Overview

This Python script is designed for web scraping using Selenium and Requests-HTML. It allows you to crawl a website, collect links, and scrape data from those links. The script uses headless mode for the Chrome browser and supports dynamic content loading.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3
- Selenium
- Requests-HTML
- ChromeDriver (compatible with your Chrome browser version)

Install the required Python libraries using:

```bash
pip install selenium requests_html
```

## How to Use

1. Replace the `starting_url` variable with the desired starting URL.

2. Run the script using the following command:

```bash
python script_name.py
```

## Features

- **get_links:** Retrieves links from a given URL, clicks on "Load More" buttons if present, and filters out links not from the same domain.

- **scrape_data:** Scrapes relevant data from a given URL using Requests-HTML. Demonstratively extracts headings and paragraphs.

- **crawl_and_scrape:** Initiates a crawl and scrape process starting from the `starting_url` with a specified maximum depth. It saves unique links and scraped data to JSON files.

## Output

- The script outputs two JSON files:
  - `output_links.json`: Contains unique links discovered during the crawl.
  - `output_data.json`: Contains scraped data including URL, headings, and paragraphs.

## Notes

- Adjust the delays and timeouts in the script based on your site's loading time.
- Make sure to replace `'starting_url'` with the actual starting URL.
- Chrome browser runs in headless mode by default. Adjust Chrome options in `get_links` if needed.

Feel free to customize the script to fit your specific requirements. Happy scraping!
