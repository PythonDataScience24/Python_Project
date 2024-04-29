import csv
import requests

# Define the SPARQL query
sparql_query = """
SELECT ?movie ?movieLabel
WHERE {
  ?movie wdt:P31 wd:Q11424.  # Instance of film
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
LIMIT 500000  # Adjust the limit as needed to retrieve more movies
"""

# Define the Wikidata Query Service endpoint
wdqs_endpoint = 'https://query.wikidata.org/sparql'

# Send the SPARQL query to Wikidata
response = requests.get(wdqs_endpoint, params={'query': sparql_query, 'format': 'json'})

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Extract movie data from the response
    movies = [(item['movieLabel']['value'], item['movie']['value']) for item in data['results']['bindings']]
    
    # Write the movies to a CSV file
    with open('movies.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['Movie Label', 'Movie ID'])
        # Write movie data
        writer.writerows(movies)
        
    print('Movies have been saved to movies.csv')
else:
    print('Failed to fetch data from Wikidata.')
