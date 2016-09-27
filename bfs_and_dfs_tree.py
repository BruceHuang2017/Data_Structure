import urllib2
from collections import deque
from BeautifulSoup import BeautifulSoup

def getLinks(url,baseurl="http://secon.utulsa.edu/cs2123/webtraverse/"):

    soup = BeautifulSoup(urllib2.urlopen(url).read())
    return [baseurl+a["href"].encode('ascii','ignore') for a in soup.findAll('a')]


def generator_dfs(url, S = None):       # dfs algorithm generator
    S, Q = set(), []                    # visited set and list
    Q.append(url)                       # start with s
    while Q:                            # s(initial) or neighbors of u(loop)
        u = Q.pop()                     # get one from nodes
        if u in S: continue             # visited node, skip
        S.add(u)                        # set u as visited node
        g = getLinks(u)                     # get list of neighbors
        g = sorted(g, key=str.lower)    # sort by a, b, c, d ... with case-insensitive string comparation
        Q.extend(g)                     # find all neighbors with u
        yield u                         # u is done, processed

def print_dfs(url):                     # use generator and print out list
    print list(generator_dfs(url))

def generator_bfs(url, S = None):       # bfs algorithm generator
    S, Q = set(), deque()               # visited set and deque
    Q.append(url)                       # start with s
    while Q:                            # s(initial) or neighbors of u(loop)
        u = Q.popleft()                 # get one from nodes
        if u in S: continue             # visited node, skip
        S.add(u)                        # set u as visited node
        g = getLinks(u)                 # get list of neighbors
        g = sorted(g, key=str.lower)    # sort by a, b, c, d ... with case-insensitive string comparation
        Q.extend(g)                     # find all neighbors with u
        yield u                         # u is done, processed

def print_bfs(url):                     # use generator and print out list
    print list(generator_bfs(url))

def bfs_parents(G, s):
    P, Q = {s: None}, deque([s])
    while Q:
        u = Q.popleft()
        for v in G[u]:
            if v in P: continue
            P[v] = u
            Q.append(v)
    return P

def find_shortest_path_printer(url1,url2):
    url = "http://secon.utulsa.edu/cs2123/webtraverse/index.html"
    node = list(generator_bfs(url))
    G = dict((u, getLinks(u)) for u in node)    # find undirected graph
    try:
        P = bfs_parents(G, url1)                        # bfs parents dictionary start with url1
        path = [url2]                           # use bfs parents dictionary P to find path between A and B
        while P[url2] != url1:          # when url1 is not next to url2
            if P[url2] is None:             # stop when url2 is root
                print 'There is no way the first url can reach the second one.'
                break
            path.append(P[url2])            # add bfs parent of url2 to path, go one step
            url2 = P[url2]                  # based on the new node, loop till reach target
        path.append(P[url2])                # add initial value
        path.reverse()                      # reverse path to start from url1
        yield path                      # instead using return path, use print path. for a function can only return one result. but can print more.
    except KeyError, e:
        pass                                #'There is no way the first url can reach the second url.'
    try:
        P = bfs_parents(G, url2)                        # bfs parents dictionary start with url1
        path = [url1]                           # use bfs parents dictionary P to find path between A and B
        while P[url1] != url2:          # when url1 is not next to url2
            if P[url1] is None:             # stop when url2 is root
                print 'There is no way the second url can reach the first one.'
                break
            path.append(P[url1])            # add bfs parent of url2 to path, go one step
            url2 = P[url1]                  # based on the new node, loop till reach target
        path.append(P[url1])                # add initial value
        path.reverse()                     # reverse path to start from url1
        yield path
    except KeyError, e:
        pass

def find_shortest_path(url1,url2):
    path = list(find_shortest_path_printer(url1,url2))
    if path == [] or path == None:
        print 'Path not found between',url1,'and',url2     #'There is no way second url can reach the first url.
    else:
        print path[0]

def find_max_depth(start_url):
    node = list(generator_bfs(start_url))
    G = dict((u, getLinks(u)) for u in node)                            # find undirected graph
    P = bfs_parents(G, start_url)
    target_url = ''
    maxl = 0
    for v in P.keys():
        if v != None and v != start_url:
            r = list(find_shortest_path_printer(start_url, v))
            if r != []:
                if maxl < len(r[0]):
                    maxl = len(r[0])
                    target_url = v
    print target_url
    path = list(find_shortest_path_printer(start_url,target_url))
    print 'Path: ', path[0]

if __name__=="__main__":
    starturl = "http://secon.utulsa.edu/cs2123/webtraverse/index.html"
    print "*********** (a) Depth-first search   **********"
    print_dfs(starturl)
    print "*********** (b) Breadth-first search **********"
    print_bfs(starturl)
    print "*********** (c) Find shortest path between two URLs ********"
    find_shortest_path("http://secon.utulsa.edu/cs2123/webtraverse/turing.html","http://secon.utulsa.edu/cs2123/webtraverse/wainwright.html")
    find_shortest_path("http://secon.utulsa.edu/cs2123/webtraverse/turing.html","http://secon.utulsa.edu/cs2123/webtraverse/dijkstra.html")
    print "*********** (d) Find the longest shortest path from a starting URL *****"
    find_max_depth(starturl)

'''
output:

*********** (a) Depth-first search   **********
['http://secon.utulsa.edu/cs2123/webtraverse/index.html', 'http://secon.utulsa.edu/cs2123/webtraverse/clink.html', 'http://secon.utulsa.edu/cs2123/webtraverse/p7.html', 'http://secon.utulsa.edu/cs2123/webtraverse/p6.html', 'http://secon.utulsa.edu/cs2123/webtraverse/p8.html', 'http://secon.utulsa.edu/cs2123/webtraverse/alink.html', 'http://secon.utuls$
*********** (b) Breadth-first search **********
['http://secon.utulsa.edu/cs2123/webtraverse/index.html', 'http://secon.utulsa.edu/cs2123/webtraverse/alink.html', 'http://secon.utulsa.edu/cs2123/webtraverse/blink.html', 'http://secon.utulsa.edu/cs2123/webtraverse/clink.html', 'http://secon.utulsa.edu/cs2123/webtraverse/dijkstra.html', 'http://secon.utulsa.edu/cs2123/webtraverse/turing.html', 'http:$
*********** (c) Find shortest path between two URLs ********
Path not found between http://secon.utulsa.edu/cs2123/webtraverse/turing.html and http://secon.utulsa.edu/cs2123/webtraverse/wainwright.html
['http://secon.utulsa.edu/cs2123/webtraverse/dijkstra.html', 'http://secon.utulsa.edu/cs2123/webtraverse/turing.html']
*********** (d) Find the longest shortest path from a starting URL *****
http://secon.utulsa.edu/cs2123/webtraverse/bletchley.html
Path:  ['http://secon.utulsa.edu/cs2123/webtraverse/index.html', 'http://secon.utulsa.edu/cs2123/webtraverse/alink.html', 'http://secon.utulsa.edu/cs2123/webtraverse/turing.html', 'http://secon.utulsa.edu/cs2123/webtraverse/kings.html', 'http://secon.utulsa.edu/cs2123/webtraverse/bletchley.html']

'''
