from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from NameHive.Ripper import getFeaturedChannels, csvWriter


def socialBlade500():
    url = "https://socialblade.com/youtube/top/trending/top-500-channels-1-day/most-subscribed"

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()

    # pass the HTML to BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    # get HTML of table called site Table where all the links are displayed
    main_table = soup.find("div", attrs={'style': 'float: right; width: 900px;'})
    # Go into main_table and get every a element in it which has class 'title'

    links = []
    names = []

    #sick ass way to get all href key values from links
    for link in main_table.find_all('a'):
        links.append(link.get('href'))
        names.append(link.get_text())

    links.pop(0) # gets rid of products link
    names.pop(0) # gets rid of premium subscription

    fixed_links = [] # need to make a new list because it wouldn't let me alter the string for some reason
    for item in links:
        fixed_links.append(item.replace('/youtube/', 'https://www.youtube.com/'))

    # combines 2 lists into dictionary
    topYoutubers = []
    i = 0
    for item in names:
        topYoutubers.append([names[i], fixed_links[i]])
        i += 1

    return topYoutubers

topYoutubers = socialBlade500()
print("Top 500 Youtubers: ", topYoutubers, '\n\n')

getFeaturedChannels(topYoutubers) # takes in top youtubers and returns "featuredYoutubers" which is all featured channels
