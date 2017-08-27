import sys
from workflow import Workflow, web


# movies in theaters
def new_movie():
    url = "https://api.douban.com/v2/movie/in_theaters"
    r = web.get(url)

    r.raise_for_status()

    movies = []
    data = r.json()
    results = data['subjects']

    for movie in results:
        movies.append(movie)
    return movies


def main(wf):
  
    movies = wf.cached_data("new_movie", new_movie, max_age=600)

    for movie in movies:
        wf.add_item(uid=movie['id'],
                    arg=movie['alt'],
                    title=movie['title'],
                    subtitle=movie['original_title'] + " " + movie['year']+"   rating: "+"{:.1f}".format(movie['rating']['average']),
                    icon="icon.jpg",
                    valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    logger = wf.logger

    sys.exit(wf.run(main))
