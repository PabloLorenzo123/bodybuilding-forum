import requests
from xml.etree import ElementTree

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

"""Utilities"""
esearch = f"{base_url}/esearch.fcgi"
esummary = f"{base_url}/esummary.fcgi"

params = {
    'db': 'pubmed',
    'term': 'bicep hypertrophy',
}

esearch_response = requests.get(esearch, params=params)
# This converts the content to a Tree object. which has every element as an object.
#print(esearch_response.content)
esearch_root = ElementTree.fromstring(esearch_response.content)

#print(ElementTree.tostring(root, encoding='utf-8').decode('utf-8'))
# print(root.findall('.//Id')[0].text)
esearch_pmids = [id_element.text for id_element in esearch_root.findall('.//Id')]
#print(pmids)

"""Esummary"""
esummary_response = requests.get(esummary, params={'db':params['db'], 'id':esearch_pmids[0]})

if esummary_response.status_code == 200:
    # Assume esummary_response contains the XML response
    # print(esummary_response.content) This is returning XML text.
    esummary_root = ElementTree.fromstring(esummary_response.content)

    date = ''
    authors = []
    title = ''
    id = esummary_root.findall('.//Id')[0].text

    for e in esummary_root.findall('.//Item'):

        attrib_name = e.attrib['Name']
        if attrib_name == 'EPubDate':
            date = e.text
        elif attrib_name == 'Author':
            authors.append(e.text)
        elif attrib_name == 'Title':
            title = e.text

    print(f"{date}\n {title[0:70]}..\n {','.join(authors)} {id}\n")
    elements = [e.attrib for e in esummary_root.findall('.//Item')]
    elements_values = [e.text for e in esummary_root.findall('.//Item')]

    # Find the AuthorList element
    # author_list_element = esummary_root.find('.//Item[@Name="AuthorList" and @Type="List"]')

    # Extract and print the names of all authors
    # authors = [author_element.text for author_element in author_list_element]

    # pmid = esummary_root.findall('.//Id')[0].text
    #print(esummary_response)
    # print(esummary_response.url)
