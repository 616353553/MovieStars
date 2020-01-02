from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import logging
from Movie import Movie
from Starring import Starring
from Actor import Actor
import json
import re


logging.basicConfig(filename="crawler.log", level=logging.WARNING,
                    format="%(asctime)s:%(levelname)s:%(message)s")

# url = "https://en.wikipedia.org/wiki/Morgan_Freeman_on_screen_and_stage"
# url = "https://en.wikipedia.org/wiki/The_Pawnbroker_(film)"
# url = "https://en.wikipedia.org/wiki/Morgan_Freeman_on_screen_and_stage"
# url ="http://www.blankwebsite.com/"
url = "https://en.wikipedia.org/wiki/Robert_Downey_Jr._filmography"
# url = "https://en.wikipedia.org/wiki/Pound_(film)"
# url = "https://en.wikipedia.org/wiki/Iron_Man_3"

url_base = "https://en.wikipedia.org"

minMovies = 125
minActors = 250

movies= {}
bad_movies = {}
actors = {}
bad_actors = {}
starrings = []


def get_page_soup(url):
    page_soup = None
    try:
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
    except ValueError:
        logging.warning("Unknown actor url({})".format(url))
    finally:
        return page_soup
    
def gross_value_formatter(gross_value_str):
    gross_value_str.encode('ascii', 'ignore')
    if "illion" in gross_value_str:
        gross_value_str = gross_value_str[:gross_value_str.index("illion") + 6]
    if "[" in gross_value_str:
        gross_value_str = gross_value_str[:gross_value_str.index("[")]
    gross_value_str = gross_value_str.replace("million", "100000")
    gross_value_str = gross_value_str.replace("billion", "100000000")
    gross_value_str = re.sub('[^0-9]','', gross_value_str)
    parts = gross_value_str.split()
    if (len(parts) >= 2):
      return str(int(float(parts[0]) * int(parts[1])))
    return gross_value_str


def crawl_movie(movie_name, movie_url):
    if movie_name in movies or movie_name in bad_movies:
        logging.info("Ignore movie \"{}\" due to looping({})".format(movie_name, movie_url))
        return [], "-1"
    page_soup = get_page_soup(movie_url)
    if page_soup is None:
        return [], "-1"
    tables = page_soup.find_all("table", {"class": "infobox vevent"})
    if len(tables) == 0:
        logging.error("Movie ignored due to bad format({})".format(movie_url))
        return [], "-1"
    # start crawling
    actor_infos = []
    for table in tables:
        # get gross value
        gross_row = table.find("th", text='Box office')
        if gross_row is None:
            logging.error("Movie ignored due to missing gross value({})".format(movie_url))
            return [], "-1"
        gross_value = gross_value_formatter(gross_row.find_next().text)
        # get starrig actors
        starring_row = table.find("th", text='Starring')
        if starring_row is None:
            logging.warning("Movie ignored due to missing starring info({})".format(movie_url))
            return [], "-1"
        starring_actors = starring_row.find_next().find_all("a")
        actor_name = ""
        actor_url = ""
        actor_weight = 0
        for (idx, starring_actor) in enumerate(starring_actors):
            actor_name = starring_actor.text.strip()
            actor_url = url_base + starring_actor["href"]
            actor_weight = len(starring_actors) - idx
            starrings.append(Starring(actor_name, movie_name, actor_weight))
            actor_infos.append((actor_name, actor_url))
        return actor_infos, gross_value




def crawl_actor(actor_name, actor_url):
    if actor_name in actors or actor_name in bad_actors:
        logging.info("Ignore actor \"{}\" due to looping({})".format(actor_name, actor_url))
        return [], "Unknown"
    page_soup = get_page_soup(actor_url)
    if (page_soup is None):
        bad_actors[actor_name] = None
        return [], "Unknown"
    # start crawling 
    birth_year = "Unknown"
    tables = page_soup.find_all("table", {"class": "infobox biography vcard"})
    if len(tables) > 0:
        for table in tables:
            born_row = table.find("th", text='Born')
            if born_row is not None:
                start = born_row.find_next().text.index("19")
                birth_year = born_row.find_next().text[start: start + 4]
                break
    tables = page_soup.find_all("table")
    if len(tables) == 0:
        logging.error("Actor ignored due to bad format({})".format(actor_url))
        bad_actors[actor_name] = None
        return [], "Unknown"
    # start crawling movies
    actor_infos = []
    for table in tables:
        ths = table.tbody.tr.find_all("th")
        headings = [th.text.strip() for th in ths]
        # movie table will have columns with name 'Title', 'Year' and 'Role'
        if set(["Title", "Year", "Role"]).issubset(headings):
            movie_rows = table.tbody.find_all("tr")
            release_year_prev = ""
            for movie_row in movie_rows[1:]:
                release_year = ""
                movie_name = ""
                movie_url = ""
                # find movie release_year
                
                movie_row_children = movie_row.findChildren(recursive=False)
                if movie_row_children is not None and len(movie_row_children) >= 2:
                    release_year = movie_row_children[0].text.strip()
                    try:
                        int(release_year)
                        release_year_prev = release_year
                        movie_name = movie_row_children[1].text.strip()
                        if movie_row_children[1].find("a") is not None:
                            movie_url = url_base + movie_row_children[1].find("a")["href"]
                    except ValueError:
                        release_year = release_year_prev
                        movie_name = movie_row_children[0].text.strip()
                        if movie_row_children[0].find("a") is not None:
                            movie_url = url_base + movie_row_children[0].find("a")["href"]
                if release_year == "" or movie_name == "" or movie_url == "":
                    logging.error("movie \"{}\" ignored due to missing info({})".format(movie_name, actor_url))
                    continue
                else:
                    sub_actor_infos, gross_value = crawl_movie(movie_name, movie_url)
                    if gross_value != "-1" and len(sub_actor_infos) > 0:
                        movies[movie_name] = Movie(movie_name, release_year, gross_value)
                        actor_infos.extend(sub_actor_infos)
                    else:
                        bad_movies[movie_name] = None
            return actor_infos, birth_year
    logging.error("Movie table not found({})".format(actor_url))
    bad_actors[actor_name] = None
    return [], "Unknown"



if __name__ == "__main__":
    actor_infos = [("Robert Downey Jr.", url)]
    while len(movies) < minMovies and len(actors) < minActors:
        if len(actor_infos) == 0:
            break
        actor_info = actor_infos.pop(0)
        sub_actor_infos, birth_year = crawl_actor(actor_info[0], actor_info[1])
        if len(sub_actor_infos) > 0 and actor_info[0] not in actors and actor_info[0] not in bad_actors:
            actors[actor_info[0]] = Actor(actor_info[0], birth_year)
        actor_infos.extend(sub_actor_infos)

    json_file = open("data.json", "w")
    movie_arr = []
    actor_arr = []
    starring_arr = []
    for key, val in movies.items():
        movie_arr.append(val.to_JSON())
    for key, val in actors.items():
        actor_arr.append(val.to_JSON())
    for val in starrings:
        starring_arr.append(val.to_JSON())
    json_file.write(json.dumps({"movies": movie_arr, "actors": actor_arr, "starrings": starring_arr}, indent=2))