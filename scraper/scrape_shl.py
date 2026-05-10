import json
import time

from bs4 import BeautifulSoup

from playwright.sync_api import (
    sync_playwright
)


BASE_URL = (
    "https://www.shl.com/"
    "products/product-catalog/"
)


OUTPUT_FILE = (
    "data/assessments.json"
)


def scrape_catalog():

    all_assessments = []

    seen_urls = set()

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        # Individual Test Solutions
        # type=1

        for start in range(0, 400, 12):

            url = (
                f"{BASE_URL}"
                f"?start={start}&type=1"
            )

            print("=" * 60)

            print(
                f"Opening page: {url}"
            )

            page.goto(
                url,
                timeout=60000
            )

            page.wait_for_load_state(
                "networkidle"
            )

            page.wait_for_timeout(5000)

            html = page.content()

            soup = BeautifulSoup(
                html,
                "lxml"
            )

            links = soup.select("a")

            page_count = 0

            for link in links:

                href = link.get("href")

                if not href:
                    continue

                if href.startswith("/"):

                    href = (
                        "https://www.shl.com"
                        + href
                    )

                if (
                    "product-catalog/view"
                    in href.lower()
                ):

                    if href in seen_urls:
                        continue

                    seen_urls.add(href)

                    name = (
                        link.get_text(
                            strip=True
                        )
                    )

                    if not name:
                        continue

                    assessment = {

                        "name": name,

                        "url": href,

                        "description": "",

                        "keywords": [],

                        "test_type": "Unknown"
                    }

                    all_assessments.append(
                        assessment
                    )

                    page_count += 1

                    print(
                        f"Found: {name}"
                    )

            print(
                f"Page assessments: "
                f"{page_count}"
            )

            # stop condition
            if page_count == 0:

                print(
                    "No more assessments."
                )

                break

        browser.close()

    print("=" * 60)

    print(
        f"Saving "
        f"{len(all_assessments)} "
        f"assessments..."
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_assessments,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("Done.")


if __name__ == "__main__":

    scrape_catalog()