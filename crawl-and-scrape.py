import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import urlparse
from requests_html import HTMLSession

def get_links(url, visited_urls, script_dir):
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        # Allow time for the page to load dynamically
        time.sleep(10)  # Adjust this delay based on your site's loading time

        # Click on a "Load More" button if it exists
        load_more_button = driver.find_elements(By.XPATH, "//button[contains(text(), 'Load More')]")
        if load_more_button:
            load_more_button[0].click()
            time.sleep(5)  # Adjust this delay as needed

        # Wait for dynamic content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//footer"))
        )

        # Extract links
        links = [a.get_attribute('href') for a in driver.find_elements(By.TAG_NAME, 'a')]

        # Filter out links not from the same domain as the starting URL
        links = [link for link in links if urlparse(link).netloc == urlparse(url).netloc]

        # Filter out visited links
        unique_links = set(links).difference(visited_urls)

        # Save valid links to a file in the script's directory
        output_links_path = os.path.join(script_dir, 'output_links.json')
        with open(output_links_path, 'a') as file:
            file.write(json.dumps(list(unique_links), indent=2))

        # Update visited_urls with the unique links
        visited_urls.update(unique_links)

        return list(unique_links)
    finally:
        if driver:
            driver.quit()

def scrape_data(url):
    session = HTMLSession()

    try:
        response = session.get(url, timeout=30)  # Increase timeout to 30 seconds

        # Render JavaScript
        response.html.render(timeout=30)  # Increase timeout to 30 seconds

        # Extract relevant data
        # For demonstration, let's extract headings and paragraphs
        data = {'url': url, 'headings': [], 'paragraphs': []}

        for heading in response.html.find('h1, h2, h3, h4, h5, h6'):
            data['headings'].append(heading.text)

        for paragraph in response.html.find('p'):
            data['paragraphs'].append(paragraph.text)

        # Save data to a file in the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_data_path = os.path.join(script_dir, 'output_data.json')
        with open(output_data_path, 'a') as file:
            file.write(json.dumps(data, indent=2))

        print(f"Scraping data from: {url}")
        print(data)
    except MaxRetries:
        print(f"Timeout for URL: {url}")

def crawl_and_scrape(start_url, max_depth=3, script_dir=None):
    if script_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    visited = set()
    to_visit = [start_url]

    while to_visit and max_depth > 0:
        url = to_visit.pop(0)
        if url not in visited:
            visited.add(url)
            links = get_links(url, visited, script_dir)

            # Scraping data for each link
            for link in links:
                scrape_data(link)

            # Add new links to to_visit list
            to_visit.extend(links)

            max_depth -= 1

if __name__ == "__main__":
    # Replace 'starting_url' with the actual starting URL
    starting_url = 'starting_url'

    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Clear existing output files
    open(os.path.join(script_dir, 'output_links.json'), 'w').close()
    open(os.path.join(script_dir, 'output_data.json'), 'w').close()

    # Run the crawling and scraping synchronously
    crawl_and_scrape(starting_url, script_dir=script_dir)
