from bs4 import BeautifulSoup
from urllib2 import urlopen
import re


def get_links_from_page(url, pattern, url_prepend=None):
    """
    input - url of page to be scraped, pattern of link to match, url_prepend since our links will be relative
    output - list of links
    """

    # Create soup
    webpage = urlopen(url).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    link_set = set()

    for link in soup.find_all("a"):
        if link.get('href'):
            if url_prepend:
                href = url_prepend + link.get('href')
            else:
                href = link.get('href')

            if re.match(pattern, href):
                link_set.add(href)

    return list(link_set)


def scrape_tracklisting_from_album_link(url):
    """
    Takes a URL as a param and returns a list of dictionaries with track information.
    The answer from shaktimaan helped me write the table parser:
    http://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
    """
    # Opens album url & creates the soup
    page = urlopen(url).read()
    album_soup = BeautifulSoup(page, 'html.parser')

    # Finds the tracklist table and creates rows
    table = album_soup.find_all("table", class_="tracklist")
    rows = table[0].find_all('tr')
    album_name = url[-16:-14]

    # Clean album name if this is the original album
    if album_name == "in":
        album_name = 1

    track_listing = []

    # Getting album release date
    info_table = album_soup.find('table', class_="infobox vevent haudio")
    release_date = info_table.find('td', class_="published").text
    if "(" in release_date:
        release_date = release_date[:release_date.find('(')]
    # Iterates through rows and returns data as a list of dictionaries.
    # We start from row 1 instead of 0 to skip the header
    # We ignore IndexErrors as some albums have an extra row with 2 columns
    #  that has information on total runtime
    for row in rows[1:]:
        try:
            cols = row.find_all('td')
            cols = [data.text.strip() for data in cols]

            song = {}
            song['volume_number'] = album_name
            song['number'] = cols[0]
            song['title'] = cols[1]
            song['artist'] = cols[2]
            song['duration'] = cols[3]
            song['now_release_date'] = release_date

            track_listing.append(song)
        except IndexError:
            continue
    return track_listing


def clean_duration(song_duration):
    """
    takes a time format of 4:20 and sets it to seconds equivalent 260
    """
    time = song_duration.split(":")
    minute = int(time[0]) * 60
    second = int(time[1])
    song_duration = minute + second
    return song_duration


def clean_artist(artist):
    """
    Converts artists with features to a list for easier spotify queries
    """
    if ' featuring ' in artist:
        artist = artist.replace(" featuring ", "|")
    if " and " in artist:
        artist = artist.replace(" and ", "|")
    if " & " in artist:
        artist = artist.replace(" & ", "|")
    if "|" in artist:
        artist = artist.split("|")
    return artist


def clean_title(title):
    """
    Removes quotes and parens from song titles
    """
    if " (" in title:
        title = title[:title.find(" (")]
    if '"' in title:
        title = title.replace('"', "")
    return title
