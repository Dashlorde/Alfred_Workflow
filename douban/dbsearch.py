# encoding: utf-8

import sys
import urllib
from workflow import Workflow, web

logger = None


# search movies
def search(query):

    # 编码，支持中文
    query = urllib.quote(query.encode('utf8')).decode('utf8')

    url = "https://api.douban.com/v2/movie/search?q=%s" % query
    r = web.get(url)

    # throw error if request failed
    r.raise_for_status()

    movies = []

    # 解析json，详情见https://developers.douban.com/wiki/?title=movie_v2#subject
    data = r.json()
    results = data['subjects']

    for movie in results:
        movies.append(movie)

    return movies




def main(wf):
    
    query = ' '.join(wf.args)
    
    def wrapper():
        return search(query)
    movies = wf.cached_data(query, wrapper, max_age=600)
    

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
