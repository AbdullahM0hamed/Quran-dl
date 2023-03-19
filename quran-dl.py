#!/bin/python

from bs4 import BeautifulSoup
from clint.textui import progress
from os.path import expanduser
import requests
import os
import subprocess
import sys

session = requests.session()

def getSelectedInput(prompt):
 try:
  choice = input(prompt)
  if choice == "":
    choice = "1"
  while not choice.isnumeric() or int(choice) <= 0:
    choice = input(prompt)
    if  choice == "":
      choice = "1"
 except KeyboardInterrupt:
   print("\033]0;\007")
   sys.exit(0)
 return int(choice)

def Download(file, name, location):
  r = session.get(file, stream=True)
  size = int(r.headers.get("content-length"))
  with open(f"{location}/{name}.mp3", "wb") as surah:
    for chunk in progress.bar(r.iter_content(chunk_size = 1024), expected_size=(size/1024) + 1):
      if chunk:
        surah.write(chunk)

r = session.get("https://quranicaudio.com/")
soup = BeautifulSoup(r.text, "html.parser")
qaris = soup.find_all("a", {'class':'ttnuIA4M9MIsH3LR7pTUN'})

for section in range(2, 5):
    r = session.get(f"https://quranicaudio.com/section/{section}/")
    soup = BeautifulSoup(r.text, "html.parser")
    qaris.extend(soup.find_all("a", {"class": "ttnuIA4M9MIsH3LR7pTUN"}))


qari_names, qari_links = [x.text for x in qaris], [x.get("href") for x in qaris]

i = 1
for j in qari_names:
  print(f"{i}: {j}")
  i += 1

choice = getSelectedInput("Enter Qari Number: ") - 1
r = session.get(f"https://quranicaudio.com{qari_links[choice]}")
soup = BeautifulSoup(r.text, "html.parser")
suwar = [x.find_all("span")[-1].text for x in soup.find_all("h5", {"class":"text-muted"})]
surah_names, surah_links = [i for a, i in enumerate(suwar) if  a%2 == 0], [x.parent.get("href") for x in soup.find_all("span", string=" Download")]

home = expanduser("~")
if not os.path.exists(f"{home}/Quran"):
  os.mkdir(f"{home}/Quran")

chQari = qari_names[choice]
if not os.path.exists(f"{home}/Quran/{chQari}"):
  os.mkdir(f"{home}/Quran/{chQari}")

for surah_name, surah_link in zip(surah_names, surah_links):
  Download(surah_link, surah_name, f"{home}/Quran/{chQari}")
