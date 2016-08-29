__author__ = 'Prince Leo'


# Importing External Modules
from bs4 import BeautifulSoup
import fnmatch
import re
import errno
import os
from shutilwhich import shutil


BaseFolder = "C:\Users\Public.PRITAM\Desktop\PYTHON PROJECT\iitg.vlab.co.in\iitg.vlab.co.in\\"
shutil.copy2("C:\Users\Public.PRITAM\Desktop\PYTHON PROJECT\iitg.vlab.co.in\index.html", "C:\Users\Public.PRITAM\Desktop\PYTHON PROJECT\iitg.vlab.co.in\iitg.vlab.co.in\index.html")

os.chdir(BaseFolder)
fo1 = open("debug.txt", "w+")


# Defining copyFile function
# srcFolder and destFolder must have end-slashes.
# If destFolder doesn't exist, it will not create it.
# If the file pre-exists, it will delete it.
def copy_file(new_filename, old_filename, src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        try:
            # Check if destFolder exists, if not, don't create destFolder.
            print "copy_file : " + dest_folder + " not found."
            # os.mkdir(dest_folder, 0o777)
        except WindowsError:
            print('WindowsError while creating ' + dest_folder)

    if os.path.isfile(src_folder + old_filename):
        # Check if source file exists

        try:
            if os.path.isfile(dest_folder + new_filename):
                if not src_folder + old_filename == dest_folder + new_filename:
                    # Check if the file pre-exists, if exists, remove it.
                    # print "Removing old " + dest_folder + new_filename
                    os.remove(dest_folder + new_filename)
            # shutil.copy2(src, dst)
            # Similar to shutil.copy(), but metadata is copied as well .
            # In fact, this is just shutil.copy() followed by copystat().
            # This is similar to the Unix command cp -p.
            shutil.copy2(src_folder + old_filename, dest_folder + new_filename)
        except shutil.Error as e1:
            # eg. src and dest are the same file
            print('Error: %s' % e1)
        except IOError as e2:
            # eg. source or destination doesn't exist
            fo1.write('IOError copy_file: %s' % e2.strerror + "\n")
            print('IOError copy_file: %s' % e2.strerror)
        except WindowsError:
            fo1.write('copy_file : WindowsError while copying ' + src_folder + old_filename + "\n")
            print('copy_file : WindowsError while copying ' + src_folder + old_filename)
    else:
        print old_filename + " : No such file in " + src_folder

#  + "Computer Science & Engineering\\"
# CurrentFolder = BaseFolder
# pattern_text = "@*"


def link_editor(title_string):
    """

    :rtype : str
    """
    string = ""
    x1 = title_string.count(':')
    for i in range(0, x1, 1):
        string += "../"
    return string


# title1 is the title string of the base page
# (next_page_folder + next_page) is complete address to the .html
# next_page is the .html link in the base page
# compare_url yields the href of the link in the base page
def compare_url(title1, next_page, next_page_folder):
    """

    :rtype : str
    """

    if os.path.exists(next_page_folder + next_page):
        page2 = open(next_page_folder + next_page)
        soup2 = BeautifulSoup(page2.read())

        title2 = soup2.title.string

        list1 = title1.split(':')
        x1 = len(list1)
        list1.reverse()
        for i in range(0, len(list1), 1):
            list1[i] = list1[i].strip()

        list2 = title2.split(':')
        x2 = len(list2)
        list2.reverse()
        for i in range(0, len(list2), 1):
            list2[i] = list2[i].strip()

        i = min({x1, x2}) - 1
        while i >= 0:
            if list1[i] == list2[i]:
                list1.remove(list1[i])
                list2.remove(list2[i])
            i -= 1

        # Nested if else to determine modified_url
        if len(list1) > len(list2) == 0:
            for i in range(0, len(list1), 1):
                list1[i] = ".."
            modified_url = '/'.join(list1) + "/index.html"

        elif len(list1) == 0 and len(list1) < len(list2):
            modified_url = '/'.join(list2) + "/index.html"

        elif len(list1) > len(list2) and not len(list2) == 0:
            for i in range(0, len(list1), 1):
                list1[i] = ".."
            modified_url = '/'.join(list1) + "/" + '/'.join(list2) + "/index.html"

        elif len(list1) < len(list2) and not len(list1) == 0:
            for i in range(0, len(list1), 1):
                list1[i] = ".."
            modified_url = '/'.join(list1) + "/" + '/'.join(list2) + "/index.html"

        elif len(list1) == len(list2) and not len(list1) == 0:
            for i in range(0, len(list1), 1):
                list1[i] = ".."
            modified_url = '/'.join(list1) + "/" + '/'.join(list2) + "/index.html"

        else:
            modified_url = "index.html"

        if re.search("topMenu", next_page):
            modified_url = modified_url.replace("index.html", next_page)

        if re.search("forum", next_page):
            modified_url = modified_url.replace("index.html", next_page)

        if re.search("html#", next_page):
            modified_url = modified_url.replace("index.html", next_page)

        return modified_url
    else:
        return "index.html#"


# print soup.title
# print soup.text
# print url


# input must be a link : eg. index.html@sub=58&brch=160.html
# folder is the full path to the folder containing index.html from which link was scrapped.
def modified_link_text(link, folder):
    url = BaseFolder + link
    if not os.path.exists(url):
        # In some cases link = "../some_folder/index.html"
        pre_url = folder + link
        elem = pre_url.split("/")
        pre_url = '\\'.join(elem)
        elem = pre_url.split("\\")
        for i in range(len(elem) - 1, 0, -1):
            if elem[i] == "..":
                elem.remove(elem[i])
                elem.remove(elem[i - 1])
        url = '\\'.join(elem)
    try:
        page = open(url)
        soup = BeautifulSoup(page.read())
        modified_link = soup.title.string.strip().partition(':')[0].strip()
        return modified_link.encode('utf-8')
    except IOError as e:
        fo1.write("IOError modified_link_text : " + str(e) + "\n")
        # print "IOError modified_link_text : " + str(e)
        return "index.html#"

# BUILDING FOLDER STRUCTURE #


def create_recursive_folder(title):

    """

    :rtype : str
    """

    if title.rpartition(":")[0] == '':
        return BaseFolder
    else:
        elem = title.split(':')
        for i in range(0, len(elem) - 1, 1):
            elem[i] = elem[i].strip()
        x = len(elem)
        elem.remove(elem[x - 1])
        elem.reverse()
        edited_title = '\\'.join(elem)
        dir_name = BaseFolder + edited_title
        try:
            # print "create_recursive_folder : " + dir_name
            os.makedirs(dir_name)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
        except WindowsError as e:
            print e
        return dir_name

for FileInFolder in os.listdir(BaseFolder):
    if fnmatch.fnmatch(FileInFolder, 'index.html'):
        print FileInFolder
        url = BaseFolder + FileInFolder
        page = open(url)
        soup = BeautifulSoup(page.read())
        folder_name = create_recursive_folder(soup.title.string)

        # CHANGING LINKS #

        for css in soup.find_all('link', attrs={'rel': re.compile("stylesheet")}):

            css['href'] = css['href'].replace(css.get('href'), link_editor(soup.title.string) + css.get('href'))

        for javascript in soup.find_all('script', attrs={'src': True}):

            javascript['src'] = javascript['src'].replace(javascript.get('src'), link_editor(soup.title.string) + javascript.get('src'))

        for video in soup.find_all('iframe', attrs={'src': True}):

            video['src'] = video['src'].replace(video.get('src'), link_editor(soup.title.string) + video.get('src'))

        for ext_link in soup.find_all('a', attrs={'href': re.compile("external")}):

            ext_link['href'] = ext_link['href'].replace(ext_link.get('href'), link_editor(soup.title.string) + ext_link.get('href'))

        for image in soup.find_all('img'):

            image['src'] = image['src'].replace(image.get('src'), link_editor(soup.title.string) + image.get('src'))

        for link in soup.find_all('a', attrs={'href': re.compile("index.html")}):
            try:
                link['href'] = link['href'].replace(link.get('href'), compare_url(soup.title.string, str(link.get('href')), BaseFolder))
            except UnicodeEncodeError as e:
                print str(e)
            except TypeError as e:
                print str(e)

        os.chdir(BaseFolder)
        fo = open("temp.html", "w+")
        text = str(soup.get_text)
        fo.write(text)
        fo.close()
        if not str(folder_name) == BaseFolder:
            shutil.move(BaseFolder + "temp.html", str(folder_name) + "\index.html")
        else:
            shutil.move(BaseFolder + "temp.html", str(folder_name) + "\\" + FileInFolder)
            os.remove(BaseFolder + FileInFolder)

fo1.close()