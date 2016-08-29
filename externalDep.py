__author__ = 'Prince Leo'


# Importing External Modules
from bs4 import BeautifulSoup
import fnmatch
import re
import os
import sys
import datetime
from collections import Counter
from shutilwhich import shutil

BaseFolder = "C:\Users\Public.PRITAM\Desktop\PYTHON PROJECT\iitg.vlab.co.in\iitg.vlab.co.in\\"


# Check if the External folder exists or not.
if not os.path.exists(BaseFolder + "external\\"):
    print "external dependency folder unavailable or unreachable :" + BaseFolder + "external\\"
    sys.exit("Please create the external folder to Continue. Exiting...")


# Creating no_internet_connection.html in external folder.
print "Creating " + BaseFolder + "external\\no_internet_connection.html"
os.chdir(BaseFolder + "external\\")
fo1 = open("no_internet_connection.html", "w+")
text = "Internet connection required to view this page."
fo1.write(text)
fo1.close()


os.chdir(BaseFolder)
fo_img = open(BaseFolder + "external_image.txt", "w+")
fo_img.write(str(datetime.datetime.now()) + "\n")
fo_js = open(BaseFolder + "external_js.txt", "w+")
fo_js.write(str(datetime.datetime.now()) + "\n")
fo_link = open(BaseFolder + "external_link.txt", "w+")
fo_link.write(str(datetime.datetime.now()) + "\n")

for FileInFolder in os.listdir(BaseFolder):
    if fnmatch.fnmatch(FileInFolder, 'inde*'):
        url = BaseFolder + FileInFolder
        page = open(url)
        soup = BeautifulSoup(page.read())

        # Changing external image links
        for image in soup.find_all('img', attrs={'src': re.compile("^http")}):
            image['src'] = image['src'].replace("http://", "external/")

            if not os.path.exists(BaseFolder + image['src']):
                fo_img.write(image['src'] + "\n")
                image['src'] = image['src'].replace(str(image.get('src')), "external/no_image.jpeg")

        # Changing external video links
        for video in soup.find_all('iframe', attrs={'src': True}):
            video['src'] = video['src'].replace("http://", "external/")

        # Changing external js links
        for javascript in soup.find_all('script', attrs={'src': True}):
            javascript['src'] = javascript['src'].replace("http://iitg.vlab.co.in///", "external/iitg.vlab.co.in/")

            if not os.path.exists(BaseFolder + javascript['src']):
                fo_js.write(javascript['src'] + "\n")

        # Changing home link references index.php to index.html
        for link in soup.find_all('a', attrs={'href': re.compile("index.php")}):
            link['href'] = link['href'].replace("http://iitg.vlab.co.in///index.php", "index.html")

        # Changing external dependency links
        for link in soup.find_all('a', attrs={'href': re.compile("^http")}):
            link['href'] = link['href'].replace("http://", "external/")

            if not os.path.exists(BaseFolder + link['href']):
                fo_link.write(link['href'] + "\n")
                link['href'] = link['href'].replace(str(link.get('href')), "external/no_internet_connection.html")

        # Changing Hashed links
        for hash_link in soup.find_all('a', attrs={'href': re.compile("html#")}):
            hash_link['href'] = hash_link['href'].replace(str(hash_link.get('href')), "index.html#")

        # Creating temp.html and saving the changes made to current file
        fo2 = open("temp.html", "w+")
        text = str(soup.get_text)
        fo2.write(text)
        fo2.close()
        shutil.move(BaseFolder + "temp.html", url)
        print "Done : externalDep.py " + FileInFolder

fo_img.write(str(datetime.datetime.now()) + "\n")
fo_img.close()
fo_js.write(str(datetime.datetime.now()) + "\n")
fo_js.close()
fo_link.write(str(datetime.datetime.now()) + "\n")
fo_link.close()

fo = open('ext_links.txt', 'w+')
with open('external_link.txt') as f:
    c = Counter(c.strip() for c in f if c.strip())
    for line in c:
        if c[line] > 1:
            line = line.replace("external/", "http://")
            fo.write(line + "\n")

f.close()

fo = open('js_links.txt', 'w+')
with open('external_js.txt') as f:
    c = Counter(c.strip() for c in f if c.strip())
    for line in c:
        if c[line] > 1:
            line = line.replace("external/", "http://")
            fo.write(line + "\n")

f.close()

fo = open('image_links.txt', 'w+')
with open('external_image.txt') as f:
    c = Counter(c.strip() for c in f if c.strip())
    for line in c:
        if c[line] > 1:
            line = line.replace("external/", "http://")
            fo.write(line + "\n")

f.close()