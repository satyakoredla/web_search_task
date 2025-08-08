import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(str)
        self.visited = set()

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            self.index[url] = soup.get_text()

            for link in soup.find_all('a'):
                href = link.get('href')
                if not href or href.startswith('#') or href.startswith('mailto:'):
                    continue
                full_url = urljoin(base_url or url, href)
                if full_url.startswith(base_url or url):
                    self.crawl(full_url, base_url=base_url or url)
        except requests.exceptions.RequestException as e:
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        return [url for url, text in self.index.items() if keyword.lower() in text.lower()]

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}")
        else:
            print("No results found.")


def main():
    crawler = WebCrawler()
    start_url = "https://example.com"
    crawler.crawl(start_url)
    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)


# --------------------- Unit Tests ---------------------
import unittest
from unittest.mock import patch, MagicMock

class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
            <a href="https://www.external.com">External</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertIn("https://example.com", crawler.index)
        self.assertIn("https://example.com/about", crawler.visited)
        self.assertNotIn("https://www.external.com", crawler.visited)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")
        crawler = WebCrawler()
        crawler.crawl("https://example.com")
        self.assertIn("https://example.com", crawler.visited)  # Still marked as visited

    def test_search(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "No match here"
        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])

    @patch('builtins.print')
    def test_print_results_found(self, mock_print):
        crawler = WebCrawler()
        crawler.print_results(["https://test.com"])
        mock_print.assert_any_call("Search results:")
        mock_print.assert_any_call("- https://test.com")

    @patch('builtins.print')
    def test_print_results_empty(self, mock_print):
        crawler = WebCrawler()
        crawler.print_results([])
        mock_print.assert_any_call("No results found.")

    @patch('requests.get')
    def test_ignore_mailto_and_fragment_links(self, mock_get):
        html = '''
        <html><body>
            <a href="mailto:test@example.com">Email</a>
            <a href="#top">Top</a>
            <a href="/page">Valid Page</a>
        </body></html>
        '''
        mock_response = MagicMock()
        mock_response.text = html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")
        self.assertIn("https://example.com/page", crawler.visited)
        self.assertNotIn("mailto:test@example.com", crawler.visited)

    @patch('requests.get')
    def test_invalid_html_handling(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><<><</html>"  # Bad HTML
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")
        self.assertIn("https://example.com", crawler.index)

    @patch('requests.get')
    def test_crawl_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("Timeout error")
        crawler = WebCrawler()
        crawler.crawl("https://slow.com")
        self.assertIn("https://slow.com", crawler.visited)

    @patch('requests.get')
    def test_duplicate_crawl_prevention(self, mock_get):
        html = '<html><a href="/about">About</a></html>'
        mock_response = MagicMock()
        mock_response.text = html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")
        crawler.crawl("https://example.com")  # Duplicate

        # Only two pages should be visited: main and /about
        self.assertEqual(len(crawler.visited), 2)

if __name__ == "__main__":
    unittest.main()
    main()
