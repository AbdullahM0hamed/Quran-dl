#!/bin/python

from bs4 import BeautifulSoup
from clint.textui import progress
from os.path import expanduser
import requests
import os
import subprocess
import sys

#Method to get numeric input only
#Non numerical inputs triggers a loop to ask for user input again
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

#Method to download
def Download(file, name, location):
  r = requests.get(file, stream=True)
  size = int(r.headers.get("content-length"))
  with open(f"{location}/{name}.mp3", "wb") as surah:
    for chunk in progress.bar(r.iter_content(chunk_size = 1024), expected_size=(size/1024) + 1):
      if chunk:
        surah.write(chunk)

#Get html of quranicaudio.com and convert to BeautifulSoup format
r = requests.get("https://quranicaudio.com/")
soup = BeautifulSoup(r.text, "html.parser")

#Find all "a" nodes of class "ttnuIA4M9MIsH3LR7pTUN"
#E.g. <a class="ttnuIA4M9MIsH3LR7pTUN">
qaris = soup.find_all("a", {'class':'ttnuIA4M9MIsH3LR7pTUN'})

#Extract the names of reciters, and links to their pages
qari_names, qari_links = [x.text for x in qaris], [x.get("href") for x in qaris]

#Loop through reciters and output, so that the user can make a selection
i = 1
for j in qari_names:
  print(f"{i}: {j}")
  i += 1

#Get choice of user
choice = getSelectedInput("Enter Qari Number: ") - 1

#Get html of the reciter's page and convert to BeautifulSoup format
r = requests.get(f"https://quranicaudio.com{qari_links[choice]}")
soup = BeautifulSoup(r.text, "html.parser")

#Find suwar on the reciter's page
suwar = [x.find_all("span")[-1].text for x in soup.find_all("h5", {"class":"text-muted"})]

#Extract names and links of suwar
surah_names, surah_links = [i for a, i in enumerate(suwar) if  a%2 == 0], [x.parent.get("href") for x in soup.find_all("span", string=" Download")]

home = expanduser("~")

#Checks if ~/Quran exists
#Creates it if it doesn't
if not os.path.exists(f"{home}/Quran"):
  os.mkdir(f"{home}/Quran")

#Chosen Qari
chQari = qari_names[choice]

#Checks if folder exists for the chosen qari
#and creates it if it doesn't
if not os.path.exists(f"{home}/Quran/{chQari}"):
  os.mkdir(f"{home}/Quran/{chQari}")

#Loops through the names and links of the suwar
#and downloads them, and then triggers media scanner
for surah_name, surah_link in zip(surah_names, surah_links):
  Download(surah_link, surah_name, f"{home}/Quran/{chQari}")
