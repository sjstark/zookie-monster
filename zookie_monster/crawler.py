import typer
import csv
import pickle
import requests
from bs4 import BeautifulSoup
from rich.progress import track, Progress, SpinnerColumn, TextColumn

from urllib.parse import urlparse, urljoin

from zookie_monster import ERRORS, __app_name__, __version__

app = typer.Typer()

# built-in sitemap parser:
from urllib.robotparser import RobotFileParser

def crawl_site(base_url) -> None:
	"""Crawl the url, starting with """

	(urls, hostnames) = get_urls_from_sitemaps(base_url)

	visited_urls = set()
	cookies = []

	while len(urls) > 0:
		url = urls.pop(0)
		visited_urls.add(url)
		print(f"Seaching: {url}")

		response = requests.get(url, headers={
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"
		})

		try:
			url_soup = BeautifulSoup(response.content, 'html.parser')
		except:
			continue

		for cookie in response.cookies:
			cookies.append({
				'url': url,
				'cookie_domain': cookie.domain,
				'cookie_name': cookie.name,
				'cookie_value': cookie.value,
			})

		link_elements = url_soup.select("a[href]")

		for link_element in link_elements:
			found_url = link_element["href"]


			if found_url.startswith('/'):
				found_url = urljoin(url, found_url)
			if found_url.endswith('/'):
				found_url = found_url[:-1]

			found_netloc = urlparse(found_url).netloc

			if ((found_netloc not in hostnames) or
			 (found_url in visited_urls) or
			 (found_url in urls)):
				continue

			urls.append(found_url)

	with open('cookies.pkl', 'wb') as f:
		pickle.dump(cookies, f)

	with open('cookies.csv', 'w', newline='') as csvfile, open('cookies.pkl', 'rb') as f:
		pickledcookies = pickle.load(f)
		fieldnames = ['url', 'cookie_domain', 'cookie_name', 'cookie_value']
		cookiewriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
		cookiewriter.writeheader()
		cookiewriter.writerows(pickledcookies)
		# cookiewriter.writerow(['Domain', 'Cookie Name', 'Value'])


		# for cookie in pickledcookies:
		# 	cookiewriter.writerow([cookie.domain, cookie.name, cookie.value])
		# # 	print(f"cookie domain = {cookie.domain}")
		# # 	print(f"cookie name = {cookie.name}")
		# # 	print(f"cookie value = {cookie.value}")
		# # 	print("******************************")

def get_urls_from_sitemaps(base_url: str) -> list[str]:
	with Progress(
		SpinnerColumn(),
		TextColumn("[progress.description]{task.description}"),
		transient=True
	) as progress:

		progress.add_task("Compiling Sitemaps", total=None)

		sitemaps = create_base_sitemaps(base_url)

		urls = [base_url]

		hostnames = {urlparse(base_url).netloc}

		while len(sitemaps) != 0:
			sitemap = sitemaps.pop()
			location = requests.get(sitemap)
			soup = BeautifulSoup(location.content, features='xml')

			additional_sitemaps = soup.select('sitemap loc')

			additional_urls = soup.select('url loc')

			for additional_sitemap in additional_sitemaps:
				sitemaps.append(additional_sitemap.text)

			for additional_url in additional_urls:
				urls.append(additional_url.text)

			parsed_sitemap = urlparse(sitemap)
			hostnames.add(parsed_sitemap.netloc)

	return (urls, hostnames)

def create_base_sitemaps(base_url: str) -> list[str]:
	rp = RobotFileParser(base_url + '/robots.txt')
	rp.read()
	sitemaps = []
	if rp.site_maps():
		sitemaps.extend(rp.site_maps())
	elif requests.get(sitemap_url := base_url + '/sitemap.xml').status_code == 200:
		sitemaps.append(sitemap_url)

	return sitemaps
