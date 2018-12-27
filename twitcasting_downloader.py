import urllib
import requests
from html.parser import HTMLParser
from tqdm import tqdm
import os

live_history_url = "https://twitcasting.tv/hanazono_serena/movie/515303535"
cwd = os.getcwd()

def get_url(url):
    fin = False
    byte_content = []
    while not fin:
        try:
            req = urllib.request.urlopen(url)
            byte_content = req.readlines()
            fin = True
        except Exception:
            fin = False
    return byte_content
    

def get_list(url):
    # get m3u8 url
    m3u8_url = ""
    byte_content = get_url(url)
    str_content = ""
    for line in byte_content:
        str_content += str(line, encoding='utf-8')
    class Parser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            nonlocal m3u8_url
            for Tuple in attrs:
                if Tuple[0] == "data-movie-url":
                    m3u8_url = Tuple[1]
                    # print("get m3u8!")
    parser = Parser()
    parser.feed(str_content)
    url_prefix = m3u8_url[:-10]

    # get m3u8 list
    byte_content = get_url(m3u8_url)
    ts_list = []
    for line in byte_content:
        string = str(line, encoding='utf-8')
        if '.ts' in string:
            ts_list.append((url_prefix, string))
    
    return ts_list

def download_file(ts_list):
    for ts in tqdm(ts_list):
        fin = False
        while not fin:
            try:
                print(os.path.join(cwd, ts[1]))
                req = urllib.request.urlretrieve(ts[0]+ts[1], os.path.join(cwd, ts[1][:-1]))
                fin = True
            except Exception:
                fin = False

ts_list = get_list(live_history_url)
download_file(ts_list)
