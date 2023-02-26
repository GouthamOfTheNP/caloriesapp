import requests
import selectorlib

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/39.0.2171.95 Safari/537.36'}


class Temperature:
	def __init__(self, city: str, country: str):
		self.city = city.replace(' ', '-')
		self.country = country.lower()

	def get(self):
		request = requests.get(f'https://www.timeanddate.com/weather/{self.country}/{self.city}', headers=HEADERS)
		source = request.text
		extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
		value = float(extractor.extract(source)["temp"].replace("\xa0°F", ""))
		return value
