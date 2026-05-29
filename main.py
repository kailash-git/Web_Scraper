import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


# This is to print section header

def print_section(title):
    print(title)

# Hacker news scraper

def hacker_news():

    print_section("HACKER NEWS")

    url = "https://news.ycombinator.com/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    headlines = []

    titles = soup.find_all("span", class_ = "titleline")

    for index, item in enumerate(titles[:10], start=1):

        try:

            title = item.text.strip()

            link = item.find("a")["href"]

            print(f"{index}. {title}")
            print(link)
            print()

            headlines.append({
                "title": title,
                "link": link
            })

        except Exception as e:

            print("Error:", e)

    return headlines


# CTFTIME scraper

def ctftime():

    print_section("UPCOMING CTF EVENTS")

    url = "https://ctftime.org/event/list/upcoming"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    html = response.text

    pattern = r'<a href="(/event/\d+)">(.*)</a>'

    matches = re.findall(pattern, html)

    events = []

    for index, match in enumerate(matches[:10], start=1):

        link = "https://ctftime.org" + match[0]

        title = match[1]

        print(f"{index}. {title}")
        print(link)
        print()

        events.append({
            "title": title,
            "link": link
        })

    return events

# The hacker news scraper

def the_hacker_news():

    print_section("THE HACKER NEWS")

    url = "https://thehackernews.com/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "lxml")

    data = []

    articles = soup.find_all("h2", class_="home-title")

    for index, article in enumerate(articles[:10], start=1):

        try:

            title = article.text.strip()

            parent = article.find_parent("a")

            if parent:

                link = parent.get("href")

                print(f"{index}. {title}")
                print(link)
                print()

                data.append({
                    "title": title,
                    "link": link
                })

        except Exception as e:

            print("Error:", e)

    return data


# Save all the results to a file

def save_results(data):

    with open("headlines.txt", "w", encoding="utf-8") as file:

        file.write("Web scraping report\n")
        file.write(f"Generated: {datetime.now()}\n\n")

        for section, articles in data.items():

            file.write(section)

            for article in articles:

                file.write(article["title"] + "\n")
                file.write(article["link"] + "\n\n")

# This is the Main logic

def main():

    hackernews_data = hacker_news()

    ctf_data = ctftime()

    thn_data = the_hacker_news()

    all_data = {
        "Hacker News": hackernews_data,
        "CTFTime": ctf_data,
        "The Hacker News": thn_data
    }

    save_results(all_data)

    print("\nResults saved to headlines.txt")

# To run from terminal

if __name__ == "__main__":

    main()


