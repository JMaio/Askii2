import os.path
import urllib2

from bs4 import BeautifulSoup


def determineType(url, phoneno, direction):
    if "/comments/" in url:
        return commentThread(url, phoneno, direction)
    else:
        return subreddit(url)


def commentThread(url, phoneno, direction):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()  # its always safe to close an open connection
    soup = BeautifulSoup(page, "lxml")
    paras = soup.select("[class~=commentarea]")
    file_text = "0"
    if os.path.exists("user_data\\" + str(phoneno) + ".txt"):
        file_text = (readFile("user_data\\" + str(phoneno) + ".txt"))
    index = int(file_text)
    path = "user_data" + '\\' + str(phoneno) + ".txt"
    writeFile(path, str(index))
    paras = paras[0].get_text().split('\n')
    if index < len(paras):
        return paras[index]
    else:
        return paras[index - 1]


def initials(text):
    data = str(text)
    words = data.split()
    if words[0].lower() == '[serious]':
        del words[0]
    return ''.join(word[0].upper() for word in words)


def subreddit(url):
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = {'User-Agent': user_agent}
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()  # its always safe to close an open connection

    soup = BeautifulSoup(page, "lxml")
    tags = soup.select("a[class~=title]")
    print tags
    links = []
    for tag in tags:
        links.append((tag.contents)[0])
    for i in range(0, len(links) - 1):
        links[i] = links[i] + " (" + initials(links[i]) + ")"

    # Store the intials and link to thread in a file for searching
    return '\n'.join(links)




def respond(url, phoneno, direction):
    return determineType(url, phoneno, direction)


def writeFile(filename, text):
    type(text)
    f = open(filename, "w")
    for line in text:
        f.write(line)
    f.close()


def readFile(filename):
    f = open(filename, 'r')
    return_data = f.readline()
    f.close()
    return return_data


if __name__ == '__main__':
    respond("https://www.reddit.com/r/AskReddit", 0, 0)
