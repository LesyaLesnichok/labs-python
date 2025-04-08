import requests
import json

class NasaImageFetcher:
    BASE_URL = 'https://images-api.nasa.gov/search'

    def __init__(self, query='sun'):
        self.query = query
        self.results = []

    def fetch(self):
        params = {
            'q': self.query,
        }

        response = requests.get(self.BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            self.results = data.get('collection', {}).get('items', [])
        else:
            raise Exception(f'No data, status code: {response.status_code}')

    def display_results(self, limit=5):
        if not self.results:
            print('No data to display.')
            return

        for item in self.results[:limit]:
            data = item.get('data', [])
            links = item.get('links', [])

            title = data[0].get('title', 'No title') if data else 'No title'
            print(f'Title: {title}')

            if links:
                for link in links:
                    href = link.get('href', 'No href')
                    print(f'Link: {href}')
            else:
                print('No links found.')

            print('-' * 40)

def main():
    query = input('Enter something to search: ')
    nasa = NasaImageFetcher(query)

    try:
        nasa.fetch()
        nasa.display_results()
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()
