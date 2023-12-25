from datetime import datetime
import requests
from xml.etree import ElementTree
import json

date_format = '%Y %b %d'
reduce_length = False

"""Utilities"""
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
esearch_url = f"{base_url}/esearch.fcgi"
esummary_url = f"{base_url}/esummary.fcgi"
efetch_url = f"{base_url}/efetch.fcgi"

pubmed_url = "https://pubmed.ncbi.nlm.nih.gov/"

params = {
    'db': 'pubmed',
    'retmax': 10,
    'retmode': 'json',
    'sort': 'Relevance',
}

# This ensures that the articles are bodybuilding related.
selected_journals = [
    'J Strength Cond Res', 'OR', 'Med Sci Sports Exerc', 'OR', 'Int J Sports Physiol Perform', 'OR', 'Eur J Appl Physiol', 'OR', 'Sports Med', 'OR',
    'J Appl Physiol', 'OR', 'J Sports Sci', 'OR', 'J Sports Sci Med', 'OR', 'Strength Cond J',
]


"""This function takes as a parameter a query, and gets to the PUBMED database and retrieve a list of the studies related to the topic."""
def create_table(query):
    q = f'{query} AND ({" ".join(selected_journals)}) '
    
    response = requests.get(
        esearch_url,
        params = {
            'db': params['db'],
            'term': query,
            'retmax': params['retmax'],
            'retmode': 'json',
            'sort': params['sort']
            }
    )
    print(q)
    if response.status_code == 200:
        esearch_json = response.json()
        # print(json.dumps(esearch_json, indent=2))
        rows = []
        for pmid in  esearch_json['esearchresult']['idlist']:
            rows.append(esummary(pmid))
        return rows
    else:
        print(f"There's been a problem for {query}, {response.status_code}")
        raise Exception(f"There's been a problem {response.status_code}")


"""Returns a row with the head content of an article based on its PMID"""
def esummary(pmid):
    """Esummary"""
    response = requests.get(
        esummary_url,
        params = {
            'db': params['db'],
            'id': pmid,
            'retmax': params['retmax'],
            'retmode': params['retmode'],
            }
    )
    
    if response.status_code == 200:

        esummary_json = response.json()
        # print(json.dumps(esummary_json, indent=2))

        id = esummary_json['result']['uids'][0]
        article = esummary_json['result'][id]

        row = {
            'id': id,
            'date': '',
            'authors': ' '.join(auth['name'] for auth in article['authors']),
            'title': article['title'],
            'url': f"{pubmed_url}{article['uid']}/",
        }

        # Date: If the date is complete save it, if it isnt try year and month, if it isnt try year.
        if 'pubdate' in article.keys():
            row['date'] = article['pubdate']
        elif 'epubdate' in article.keys():
            row['date'] = article['epubdate']

        try:
            row['date'] = datetime.strptime(row['date'], date_format).date()
        except:
            try:
                row['date'] = datetime.strptime(row['date'], '%Y %b').date()
            except:
                try:
                    row['date'] = datetime.strptime(row['date'], '%Y').date()
                except:
                    row['date'] = row['date']
 
        # Add the study details (abstract, results, conclusions.)
        row['study'] = get_abstract(row['id'])
        return row
    else:
        raise Exception(f"There's been a problem {response.status_code}")


"""This functions gets the abstract of a PMID"""
def get_abstract(pmid):
    efetch_response = requests.get(
        efetch_url,
        params = {
            'db': params['db'],
            'id': pmid
            }
    ) # Efect can't return JSON.
    
    result = {'abstract': '', 'results': '', 'conclusion': '', 'debug': efetch_response.url}

    if efetch_response.status_code == 200:
        efect_root = ElementTree.fromstring(efetch_response.content)

        for a in efect_root.findall('.//AbstractText'):
            if 'Label' not in a.attrib.keys():
                continue
            elif a.attrib['Label'] == 'RESULTS':
                # Get recursevily all its content.
                for suba in a.itertext():
                    result['results'] += suba
            elif a.attrib['Label'] == 'CONCLUSIONS':
                result['conclusion'] = a.text

        # Abstract
        abstractText = efect_root.findall('.//AbstractText')
        if len(abstractText) > 0:
            for a in abstractText:
                result['abstract'] += a.text
        else:
            print(efetch_response.url)

        return result
    else:
        raise Exception(f"There's been a problem {efetch_response.status_code} {efetch_response.url}")
    