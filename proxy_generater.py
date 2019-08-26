from bs4 import BeautifulSoup
from random import choice
import requests

def get_proxy():
    """
    To generate proxy ip and port from url = 'https://www.sslproxies.org/'
    """
    url = 'https://www.sslproxies.org/'
    
    # Retrieve the site's page. The 'with'(Python closure) is used here in order to automatically close the session when done
    r = requests.get(url)
        
    # Create a BeutifulSoup object and find the table element which consists of all proxies
    soup = BeautifulSoup(r.content, 'html.parser')

    return {"https":choice(list(map(lambda x: x[0]+":"+x[1],list(zip(map(lambda x: x.text, soup.findAll('td')[::8]), 
                                                          map(lambda x: x.text, soup.findAll('td')[1::8]))))))}
                   
       

def proxy_request(request_type, url, **kwargs):
    """
    To generate  proxy request
    """
    while True:
        try:
            proxy = get_proxy()
            r = requests.request(request_type, url, proxies = proxy, timeout = 5, **kwargs)
            break
        except:
            pass
    return r
