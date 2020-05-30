from multiprocessing import Pool
from queue import Queue
from bs4 import BeautifulSoup
import copy
import requests
import urllib


def links_from_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    content = soup.find("div", {"id": "mw-content-text"})
    links = content.find_all("a")
    for link in links:
        href = link.get('href', '')
        #  если это страница википедии
        if href.startswith('/wiki'):
            href = urllib.parse.unquote(href)
            #  если это не файл и не служебная страница
            if (not href.startswith('/wiki/Файл:'))\
                    and (not href.startswith('/wiki/Служебная:')):
                #  если этоо подстраница, то вернём основную
                if '#' in href:
                    href = href.split('#')[0]
                yield href[6:]


class LinkVertex:
    def __init__(self, from_vertex, current_vertex, to_vertices):
        self.from_vertex = from_vertex
        self.current_vertex = current_vertex
        self.to_vertices = to_vertices


def vertices_in_parallel(curr_article):
    to_verts = []
    curr_article = "https://ru.wikipedia.org/wiki/" + curr_article
    r = requests.get(curr_article)
    if r.status_code != 200:
        r = requests.get(curr_article)
    for i in links_from_text(r.text):
        to_verts.append(i)
    return set(to_verts)


def shortest_path(from_article: str, to_article: str, n_threads: int):
    q = Queue()
    print("from: " + from_article + "\n to: " + to_article)
    if from_article == to_article:
        return [[]]
    from_article = from_article
    q.put(LinkVertex(None, None, [from_article]))
    all_sh_paths = []
    find = False
    while q.empty() is False:
        curr = q.get()
        vertex_buf = []

        with Pool(n_threads) as p:
            vertices = list(curr.to_vertices)
            for ind, atrs in enumerate(p.map(vertices_in_parallel, vertices)):
                for i in atrs:
                    if i == to_article:
                        find = True
                        path = [i]
                        if vertices[ind] != from_article:
                            path.append(vertices[ind])
                        buf = curr.from_vertex
                        while buf is not None:
                            if buf.current_vertex is not None:
                                path.append(buf.current_vertex)
                            buf = buf.from_vertex
                        all_sh_paths.append(copy.deepcopy(path[::-1]))
                vertex_buf.append(LinkVertex(curr, vertices[ind], atrs))
        if find is False:
            for i in vertex_buf:
                q.put(i)
    return all_sh_paths
