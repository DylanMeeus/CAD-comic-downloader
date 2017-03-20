import sys
import urllib, urllib2
import os
from datetime import date,datetime
from bs4 import BeautifulSoup

""" Program to download all the cad-comics (ctrl+alt+del comics)
    If you like the comics, considering becoming a Patreon of Tim: https://www.patreon.com/CtrlAltDel
    I am in no way affiliated with CAD-comics, but feel that if you use this program, you should consider becoming a patron,
    because Tim will miss out on revenue made through ads of his website."""

# Pass some headers, so the server allows our requests.
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection' : 'keep-alive'}

baseUrl = "http://www.cad-comic.com"

global scrapingYear # The year we are scraping
global index # The index of the comic for the given year

def scrape(partialComicURL):
    global scrapingYear
    global index

    site = baseUrl + partialComicURL
    request = urllib2.Request(site,headers=hdr)
    f = urllib2.urlopen(request)
    soup = BeautifulSoup(f.read(),'html.parser')

    # Find the image source
    contentDiv = soup.find(id="content")
    imageSource = contentDiv.find_all('img')[0]["src"] # src attribute of first element in the array (only one result for the URL)
    imageRequest = urllib2.Request(imageSource,headers=hdr)

    # format filename, jus take the last part of the comic (after 2nd slash of partial)
    extension = imageSource[-3:]
    filename = str(index) + " : " + (partialComicURL.split("/")[2]) + "." + extension
    index+=1

    #Write the image to a file
    f = open(scrapingYear+"/"+filename,"wb")
    f.write(urllib2.urlopen(imageRequest).read())
    f.close()
    return


""" Scrape an archive for a given year, retrieves all the comic URLs for this year."""
def scrapeArchiveForComics(year):
    print year
    global scrapingYear
    global index
    index = 0 # We set the index to 0 again, because we are fetching a new year of comics
    scrapingYear = year
    archiveUrl = "http://www.cad-comic.com/cad/archive/" + year

    # Look for all the URLs (a-tags) containing '2002'
    request = urllib2.Request(archiveUrl,headers=hdr);
    req = urllib2.urlopen(request)
    soup = BeautifulSoup(req.read(),'html.parser')
    aTags = soup.find_all("a")
    comicTags = filter(urlContainsYear,aTags)
    comicUrls = map(mapFetchHrefFromImageUrl,comicTags)
    # These are sorted by how they appear in the archive. They need to be reversed (last on archive = first chronologically)
    return (list(reversed(comicUrls)))


def urlContainsYear(url):
    global scrapingYear
    stringUrl = str(url) # Because BeautifulSoup makes it a 'Tag'-object normally
    return scrapingYear in stringUrl

def mapFetchHrefFromImageUrl(imgUrl):
    return str(imgUrl["href"])


""" main method to download for year"""
def downloadForYear(year):
    comicUrls = scrapeArchiveForComics(year)
    try:
        os.mkdir(year) # Create a folder to store the comics.
    except OSError:
            pass # the folder already exists, should we maybe empty it?

    i = 0
    for comic in comicUrls:
        print "Scraping CAD-comic #" + str(i) + " from: " + str(len(comicUrls)) + " for year: " + year
        scrape(comic)
        i+=1


def main():
    if len (sys.argv) > 1:
        year = sys.argv[1]
        if year == "all":
            startYear = int(sys.argv[2]) if len (sys.argv) == 3 else 2002
            print "Scraping for all years"
            thisYear = datetime.now().year
            yearRange = range(startYear,thisYear+1) # +1 to include the current year. Otherwise range is not-inclusive
            for archiveYear in yearRange:
                downloadForYear(str(archiveYear))
            print "Done!"
        else:
            print "Scraping for year: " + year
            downloadForYear(str(year))
            print "Done!"
    else:
        print "Pass a year or _all_, starting from 2002 (sample usage: python main.py 2002, python main.py all, python main,py all 2006)"

main()





















