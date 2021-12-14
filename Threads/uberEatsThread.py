# This thread is spawned for each uber eats link that is intercepted.
# The thread will fill out its purpose of providing the link to the user and killing the link and itself after.
import os

def uberEatsThread(link):
    linkPath = os.path.join('UberEatsApps','tmp','links.txt')

    #Add the link to the links file.
    with open(linkPath,'a') as f:
        if os.path.getsize(linkPath) == 0:
            f.write("\n"+link)
        else:
            f.write(link)

    #Web scrape the page to find the ETA.

    #Infinite loop that will only break when the page is changed (food delivered)