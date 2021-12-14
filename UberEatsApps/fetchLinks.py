import os
def fetchLinks():
    try:
        uberEatsLinks = []
        with open(os.path.join('UberEatsApps','tmp','links.txt'),'r') as f:
            links = f.readlines()
            if links is None:
                raise Exception("No links.")
            for link in links:
                link = link.split(" ")
                uberEatsLinks.append([link[0],link[1]])
        return uberEatsLinks
    except Exception as a:
        print(a)
        print(os.path.abspath(__file__))
        return False