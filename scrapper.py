from lxml import html, etree
from proxy_generater import proxy_request
from filehandler import download_youtube_file, downloadFile
from bs4 import BeautifulSoup
import os
import urllib.request
from selenium import webdriver
import re
import numpy as np
from itertools import cycle
import random
import logging
import sys


def scrapper_newsflare(no_of_pages=None, search_condition=None, sort_condition=None):
    """
    This scrapper is used to scrape mp4 file from https://www.newsflare.com/search
    """
    
    if search_condition is None:
        search_condition = "accidents"
    if sort_condition is None:
        sort_condition = "newest"
    
    url = "https://www.newsflare.com/search?q="+search_condition +"&sort="+ sort_condition+ "&page={}"

    #for deciding the number of pages
    if no_of_pages is None:
        cur_page_no=1
        while True:
            page = proxy_request('get', url.format(cur_page_no))
            #page = requests.get(url.format(cur_page_no))
            fetched_page_no = int(page.__dict__.get('url').split('&')[-1].split('=')[-1])
            print("Current page no:{} Fatched_page_no{}".format(cur_page_no, fetched_page_no))
            if fetched_page_no < cur_page_no:
                #print("breaking")
                break
            cur_page_no = cur_page_no+100
    else:
        cur_page_no = no_of_pages
        page = proxy_request('get', url.format(cur_page_no))
        #page = requests.get(url.format(cur_page_no))
        fetched_page_no = int(page.__dict__.get('url').split('&')[-1].split('=')[-1])

    site_url ="https://www.newsflare.com"
    for p in np.arange(start = 1, stop = fetched_page_no+1 , step = 1):
        
        page = proxy_request('get', url.format(p))
        
        #print("pass")
        c = page.content
        soup= BeautifulSoup(c,"lxml")
        #Set to save the video link
        vid_links = set()
        r = soup.find("div", {"id": "search_results"})

        vid_ref = set((site_url + ref['href']) for ref in r.find_all("a", href=True))
        pattern = r"https://.*mp4"

        #f = open("links.txt", "a")
        print("Downloading from link:-->{}".format(url.format(p)) )

        
        for v_ref in vid_ref:
            filename = v_ref.split("/")[-1]
            vid_page = proxy_request('get', v_ref)
            html = vid_page.content
            v_soup= BeautifulSoup(html,"lxml")
            print("="*50)
            print("--->{}".format(v_ref))
            v_page = str(v_soup)
            vid_link = re.findall(pattern, v_page)
            
            for link in vid_link:
                vid_links.add(link)
                downloadFile(link, filename=filename)

def scrapper_dashcamstore():
    """
    This is an example of function to download youtube file from "https://www.thedashcamstore.com/"

    """
    url = "https://www.thedashcamstore.com/dashcam-accident-videos/"
    r = proxy_request('get', url)
    #print("pass-->1")
    c= r.content

    soup = BeautifulSoup(c, 'lxml')

    pattern_embed_playlist = r"(?:https?:\/\/)?(?:youtu\.be\/|(?:www\.|m\.)?youtube\.com\/(?:watch|v|embed)(?:\.php)?(?:\?.*v=|\/))([a-zA-Z0-9\-_]+.)+"
    pattern_embed = r"(?:http(?:s)?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:(?:watch)?\?(?:.*&)?v(?:i)?=|(?:embed|v|vi|)\/))([^\?&\"'<> #]+)"

    videos_id = re.findall(pattern_embed, str(soup))
    videos_playlist = re.findall(pattern_embed_playlist, str(soup))

    indices_playlist = [i for i, x in enumerate(videos_id) if x == "videoseries"]
    #playlist_id =  list(operator.itemgetter(* )(videos_playlist))
    playlist_id =[]
    for i in indices_playlist:
        playlist_id.append(videos_playlist[i])

    videos_id.remove('videoseries')
    download_youtube_file(videos_id)


if __name__=='__main__':
    #Example to download mp4 files from site_url ="https://www.newsflare.com"
    scrapper_newsflare()

    #Example to scrape youtube video from "https://www.thedashcamstore.com/"
    scrapper_dashcamstore()