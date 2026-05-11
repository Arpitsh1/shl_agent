import json
import time

from bs4 import BeautifulSoup

from playwright.sync_api import sync_playwright


BASE_URL = (
    "https://www.shl.com/"
    "products/product-catalog/"
)

OUTPUT_FILE = (
    "data/assessments.json"
)


def scrape_assessment_details(page, url):

    try:

        page.goto(
            url,
            timeout=60000
        )

        page.wait_for_load_state(
            "networkidle"
        )

        page.wait_for_timeout(3000)

        html = page.content()

        soup = BeautifulSoup(
            html,
            "lxml"
        )

        title = ""

        title_tag = soup.find("h1")

        if title_tag:
            title = title_tag.get_text(
                strip=True
            )

        description = ""

        meta_desc = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if meta_desc:

            description = meta_desc.get(
                "content",
                ""
            ).strip()

        full_text = soup.get_text(
            " ",
            strip=True
        ).lower()

        test_type = "Unknown"

        if "simulation" in full_text:
            test_type = "Simulation"

        elif "personality" in full_text:
            test_type = "Personality"

        elif "cognitive" in full_text:
            test_type = "Cognitive"

        elif "technical" in full_text:
            test_type = "Technical"

        elif "ability" in full_text:
            test_type = "Ability"

        keywords = []

        keyword_bank = [

            "java",
            "python",
            "sql",
            "javascript",
            "react",
            "angular",
            "aws",
            "cloud",
            "docker",
            "kubernetes",
            ".net",
            "c#",
            "data analysis",
            "leadership",
            "communication",
            "personality",
            "cognitive",
            "problem solving",
            "customer service",
            "sales",
            "backend",
            "frontend",
            "software engineer"
        ]

        for keyword in keyword_bank:

            if keyword.lower() in full_text:

                keywords.append(keyword)

        return {

            "name": title,

            "url": url,

            "description": description,

            "keywords": list(set(keywords)),

            "test_type": test_type
        }

    except Exception as e:

        print(f"ERROR scraping {url}")

        print(e)

        return None


def scrape_catalog():

    all_assessments = []

    seen_urls = set()

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        catalog_links = []

        for start in range(0, 400, 12):

            url = (
                f"{BASE_URL}"
                f"?start={start}&type=1"
            )

            print("=" * 60)

            print(f"Opening catalog: {url}")

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

                    catalog_links.append(href)

                    page_count += 1

            print(
                f"Collected links: {page_count}"
            )

            if page_count == 0:

                break

        print("=" * 60)

        print(
            f"TOTAL LINKS: "
            f"{len(catalog_links)}"
        )

        for idx, link in enumerate(catalog_links):

            print("=" * 60)

            print(
                f"[{idx+1}/"
                f"{len(catalog_links)}]"
            )

            print(link)

            data = scrape_assessment_details(
                page,
                link
            )

            if data:

                all_assessments.append(
                    data
                )

                print(
                    f"Saved: {data['name']}"
                )

            time.sleep(1)

        browser.close()

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

    print("=" * 60)

    print(
        f"Saved "
        f"{len(all_assessments)} "
        f"assessments."
    )


if __name__ == "__main__":

    scrape_catalog()