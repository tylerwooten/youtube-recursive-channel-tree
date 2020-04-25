import csv
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


#---------------------- GET FEATURED CHANNELS -------------------------#

def getFeaturedChannels(youtubers):
    # Youtube is weird and changed the name of classes after scrapping. so to trouble shoot be sure to print out the soup and find the class tag again
    iteration = 0;
    for item in youtubers:
        iteration += 1;
        try:
            url = item[1] #grabs url
            print(url, "rank: ", iteration)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #spoofs using user agent
            html = urlopen(req).read() # get the html

            # pass the HTML to BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            # get HTML of table on far right - Related and sponsored channels
            main_table = soup.find("div", class_="branded-page-v2-secondary-col")
            links = []
            names = []

            # grab all anchor tags in this table
            yt = main_table.find_all('a', class_="yt-uix-sessionlink")
            for x in yt:
                if x.get("title") is not None:
                    links.append(x.get("href"))  # take the links and throw them in links
                    names.append(x.get("title"))  # take the titles and throw them in names

            # add beginning of url portion
            fixed_links = []
            for link in links:
                if "/channel/" in link:
                    fixed_links.append(link.replace('/channel/', 'https://www.youtube.com/channel/'))
                elif "/user/" in link:
                    fixed_links.append(link.replace('/user/', 'https://www.youtube.com/user/'))

            # combining two lists into a list of lists, [name, fixed_link]
            featuredYoutubers = []
            i = 0
            for item in names:
                featuredYoutubers.append([names[i], fixed_links[i]])
                i += 1

            print("Featured Youtubers: ", featuredYoutubers)
            csvWriter(featuredYoutubers)
        except Exception:
            pass




#------------------------- CSV SECTION -------------------------------#
def csvWriter(youtubers):
    x = []
    with open('youtube_database.csv', 'r', encoding='utf-8', newline='') as csv_file:

        reader = csv.reader(csv_file)
        for channel in reader:
            x.append(channel[0])  # uses channel name to see if this item is already in my database

    new_counter = 0
    dup_counter = 0

    with open('youtube_database.csv', 'a', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        #writer.writerow(['Channel', 'Link']) #uncomment this to rewrite header

        for item in youtubers:
            if item[0] in x:
                dup_counter += 1
            else:
                writer.writerow(item)
                new_counter += 1
        print("wrote: ", new_counter)
        print("found duplicates: ", dup_counter, '\n')
#------------------------RUNNER-------------------------------#

#TopYoutubers = [[ "JeromeASF", "https://www.youtube.com/user/JeromeASF"], ['JeromeASF - Roblox', 'https://www.youtube.com/channel/UCXnZRyqhMZlydNijw_nUpvg']]

#getFeaturedChannels(topYoutubers) # takes in top youtubers and returns "featuredYoutubers" which is all featured channels
