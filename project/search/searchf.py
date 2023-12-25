from datetime import datetime
import requests
from xml.etree import ElementTree

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
    'retmax': 3,
}

# This ensures that the articles are bodybuilding related.
keywords = ['1RM', 'weight lifting', 'strenght', 'fitness', 'weight trainning']


"""This function takes as a parameter a query, and gets to the PUBMED database and retrieve a list of the studies related to the topic."""
def create_table(query):
    q = f'{query} AND {" OR ".join(keywords)}'
    
    esearch_response = requests.get(
        esearch_url,
        params = {
            'db': params['db'],
            'term': query,
            'retmax': params['retmax'],
            }
    )

    print(q, esearch_response.url)
    if esearch_response.status_code == 200:
        esearch_root = ElementTree.fromstring(esearch_response.content)
        esearch_pmids = [id_element.text for id_element in esearch_root.findall('.//Id')]

        rows = []
        for pmid in esearch_pmids:
            rows.append(esummary(pmid))
        
        return rows
    else:
        print(f"There's been a problem for {query}, {esearch_response.status_code}")
        raise Exception(f"There's been a problem {esearch_response.status_code}")


"""Returns a row with the head content of an article based on its PMID"""
def esummary(pmid):
    """Esummary"""
    esummary_response = requests.get(
        esummary_url,
        params = {
            'db': params['db'],
            'id': pmid,
            'retmax': params['retmax']
            }
    )
    
    if esummary_response.status_code == 200:

        esummary_root = ElementTree.fromstring(esummary_response.content)

        row = {
            'date': '',
            'title': '',
            'authors': [],
            'id': esummary_root.findall('.//Id')[0].text,
            'study': {},
        }

        row['url'] = f"{pubmed_url}{row['id']}/",

        for e in esummary_root.findall('.//Item'):

            attrib_name = e.attrib['Name']

            if attrib_name == 'PubDate':
                # If the date is complete save it, if it isnt try year and month, if it isnt try year.
                try:
                    row['date'] = datetime.strptime(e.text, date_format).date()
                except:
                    try:
                        row['date'] = datetime.strptime(e.text, '%Y %b').date()
                    except:
                        try:
                            row['date'] = datetime.strptime(e.text, '%Y').date()
                        except:
                            row['date'] = e.text

            elif attrib_name == 'Author':
                row['authors'].append(e.text)

            elif attrib_name == 'Title':
                row['title'] = e.text
    
            row['authors'] = ','.join(row['authors'])
 
        # Add the study details (abstract, results, conclusions.)
        row['study'] = get_abstract(row['id'])
        return row
    else:
        raise Exception(f"There's been a problem {esummary_response.status_code}")


"""This functions gets the abstract of a PMID"""
def get_abstract(pmid):
    efetch_response = requests.get(
        efetch_url,
        params = {
            'db': params['db'],
            'id': pmid}
            )
    
    result = {'abstract': '', 'results': '', 'conclusion': '', 'debug': efetch_response.url}

    if efetch_response.status_code == 200:
        efect_root = ElementTree.fromstring(efetch_response.content)

        for a in efect_root.findall('.//AbstractText'):
            if 'Label' not in a.attrib.keys():
                continue
            if a.attrib['Label'] == 'CONCLUSIONS':
                result['conclusion'] = a.text
            elif a.attrib['Label'] == 'RESULTS':
                result['results'] += a.text

        return result
    else:
        print(f'Too many requests {efetch_response.status_code}')
        raise Exception(f"There's been a problem {efetch_response.status_code} {efetch_response.url}")
    