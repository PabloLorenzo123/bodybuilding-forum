# from ai_search import explain_article
import requests
from xml.etree import ElementTree


"""Utilities"""
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
esearch_url = f"{base_url}/esearch.fcgi"
esummary_url = f"{base_url}/esummary.fcgi"
efetch_url = f"{base_url}/efetch.fcgi"

pubmed_url = "https://pubmed.ncbi.nlm.nih.gov/"

params = {
    'db': 'pubmed',
    'retmax': 10,
}

"""This function takes as a parameter a query, and gets to the PUBMED database and retrieve a list of the studies related to the topic."""
def create_table(query):

    esearch_response = requests.get(esearch_url, params={'db': params['db'], 'term': query, 'retmax': params['retmax']})
    esearch_root = ElementTree.fromstring(esearch_response.content)
    esearch_pmids = [id_element.text for id_element in esearch_root.findall('.//Id')]

    rows = []
    for pmid in esearch_pmids:
        rows.append(esummary(pmid))
    print(rows)


"""Returns a row with the head content of an article based on its PMID"""
def esummary(pmid):
    """Esummary"""
    esummary_response = requests.get(esummary_url, params={'db': params['db'], 'id': pmid, 'retmax': params['retmax']})

    if esummary_response.status_code == 200:

        esummary_root = ElementTree.fromstring(esummary_response.content)

        row = {
            'date': '',
            'title': '',
            'authors': [],
            'id': esummary_root.findall('.//Id')[0].text,
            'url': '',
        }

        for e in esummary_root.findall('.//Item'):

            attrib_name = e.attrib['Name']
            if attrib_name == 'PubDate':
                row['date'] = e.text
            elif attrib_name == 'Author':
                row['authors'].append(e.text)
            elif attrib_name == 'Title':
                if len(e.text) > 50:
                    row['title'] = e.text[0:50] + ".."
                else:
                    row['title'] = e.text
        
        # If there are too many authors.
        if len(row['authors']) > 4:
            row['authors'] = ','.join(row['authors'][:4]) + '..'
        else:
            row['authors'] = ','.join(row['authors'])
        
        # Add the URL.
        row['url'] = f"{pubmed_url}{row['id']}/"
        return row
    else:
        raise Exception("There's been a problem")


"""This functions gets the abstract of a PMID"""
def get_abstract(pmid):
    efect_request = requests.get(efetch_url, params={'db': params['db'], 'id': pmid})
    print(efect_request.url)

    result = {'abstract': '', 'conclusion': '', 'ai_explanation': ''}

    if efect_request.status_code == 200:
        efect_root = ElementTree.fromstring(efect_request.content)
        
        for a in efect_root.findall('.//AbstractText'):
            if a.attrib['Label'] == 'CONCLUSIONS':
                result['conclusion'] = a.text
            else:
                result['abstract'] += a.text

        return result
