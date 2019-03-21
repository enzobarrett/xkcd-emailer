#! python3
# downloadXkcd.py - Downloads every single XKCD comic.

import requests, os, bs4, re, sys

url = 'http://xkcd.com'              # starting url
os.makedirs('xkcd', exist_ok=True)   # store comics in ./xkcd
prevnum = 2124+1
while not url.endswith('#'):
    # Download the page.
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, features="lxml")

    # Find the URL of the comic image.
    comicElem = soup.select('#comic img')
    numberElem = soup.select('#middleContainer')
    # Find all numbers in text 
    reElem = re.findall('\d+?\d*', numberElem[0].text)
    x = 0

    # Loop through found numbers until the right one is found
    while int(prevnum)-1 != int(reElem[x]):
        if int(reElem[x]) == 403:
            prevnum = int(prevnum)-1
            break
        x+=1

    # Define the number
    number = reElem[x]
    
    # Check for the right number
    if int(prevnum)-1 != int(number):
        raise ValueError('Wrong number!')
    prevnum = number
    
    if comicElem == []:
         print('Could not find comic image.')
    else:
         try:
             comicUrl = 'http:' + comicElem[0].get('src')
             # Download the image.
             res = requests.get(comicUrl)
             res.raise_for_status()
         except requests.exceptions.MissingSchema:
             # skip this comic
             prevLink = soup.select('a[rel="prev"]')[0]
             url = 'http://xkcd.com' + prevLink.get('href')
             continue

    # Append the comic number and put back on extension
    extension = os.path.basename(comicUrl)[-4:]
    filename = os.path.join('xkcd', os.path.basename(comicUrl)[:-4] + '-' + number + extension)
    print(filename)
    
    # Save the image to ./xkcd.
    imageFile = open(filename, 'wb')
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()

    # Get the Prev button's url.
    prevLink = soup.select('a[rel="prev"]')[0]
    url = 'http://xkcd.com' + prevLink.get('href')

print('Done.')
