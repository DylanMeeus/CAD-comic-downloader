import sys
import urllib, urllib2
import os
from bs4 import BeautifulSoup

""" Program to download all the cad-comics (ctrl+alt+del comics)
    If you like the comics, considering becoming a Patreon of Tim: https://www.patreon.com/CtrlAltDel
    I am in no way affiliated with CAD-comics, but feel that if you use this program, you should consider becoming a patron
    Because Tim will miss out on revenue made through ads of his website."""

# Pass some headers, so the website allows our requests.
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection' : 'keep-alive'}

baseUrl = "http://www.cad-comic.com"

global scrapingYear # The year we are scraping

def scrape(partialComicURL):
    global scrapingYear
    print "Scraping CAD-comics.."
    site = baseUrl + partialComicURL
    request = urllib2.Request(site,headers=hdr)
    f = urllib2.urlopen(request)
    soup = BeautifulSoup(f.read(),'html.parser')

    # Find the image source
    contentDiv = soup.find(id="content")
    imageSource = contentDiv.find_all('img')[0]["src"] # src attribute of first element in the array (only one result for the URL)
    imageRequest = urllib2.Request(imageSource,headers=hdr)

    # format filename, jus take the last part of the comic (after 2nd slash of partial)
    filename = (partialComicURL.split("/")[2])+"jpg"


    # Write the image to a file
    f = open(scrapingYear+"/"+filename,"wb")
    f.write(urllib2.urlopen(imageRequest).read())
    f.close()
    return


""" Scrape an archive for a given year, finds retrieves all the comic URLs for this year."""
def scrapeArchiveForComics(year):
    print year
    global scrapingYear
    scrapingYear = year
    archiveUrl = "http://www.cad-comic.com/cad/archive/" + year

    # Look for all the URLs (a-tags) containing '2002'
    request = urllib2.Request(archiveUrl,headers=hdr);
    req = urllib2.urlopen(request)
    soup = BeautifulSoup(req.read(),'html.parser')
    aTags = soup.find_all("a")
    comicTags = filter(urlContainsYear,aTags)
    comicUrls = map(mapFetchHrefFromImageUrl,comicTags)
    print comicUrls
    return comicUrls


def urlContainsYear(url):
    global scrapingYear
    stringUrl = str(url) # Because BeautifulSoup makes it a 'tag' normally
    return scrapingYear in stringUrl

def mapFetchHrefFromImageUrl(imgUrl):
    return str(imgUrl["href"])


""" main method to download for year"""
def downloadForYear(year):
    comicUrls = scrapeArchiveForComics("2002")
    try:
        os.mkdir(year) # Create a folder to store the comics.
    except OSError:
            pass # the folder already exists, should we maybe empty it?
    for comic in comicUrls:
        scrape(comic)

downloadForYear("2002")
#scrape()

# todo : give number according to order they should be read in? Possible by comparing the date