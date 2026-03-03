# -*- coding: utf-8 -*-
"""
Script available under the MIT license
Copyright (c) 2023-2025 Philippe Gambette and Beatrice Mundo
"""

import csv, glob, os, re, sys, time
from xml.dom import minidom

# Get the current folder
folder = os.path.abspath(os.path.dirname(sys.argv[0]))

# Open the input list of identifiers
file = "OCR_tome1_1id.txt"
print(file)
inputIdFile = open(file, "r", encoding="utf-8")
letterIds = {}
for line in inputIdFile:
   letterIds[line.replace("\n","").replace("\r","")] = "1"
print(letterIds)

# Open the input text file
file = "OCR_tome1_1.txt"
print(file)
inputFile = open(file, "r", encoding="utf-8")
outputFileA = open(file+".appendix.html", "w", encoding="utf-8")
documentLineNb = 0
letters = []
letter = {}
letter["id"] = ""
letter["text"] = ""
letter["date"] = ""
letter["source"] = ""
letter["destinataire"] = ""

remplacements=[
   ["filz", "fils"]
]
def normaliseTexte(ligne):
   for remplacement in remplacements:
      ligne=ligne.replace(remplacement[0],remplacement[1])
   return ligne

def nettoieLigne(ligne):
   # remove whitespace starting the line
   res = re.search("^ (.*)",ligne)
   if res:
      ligne = res.group(1)
   
   # remove all tags between < and >
   res = re.search("(.*)<[^>]+>(.*)",ligne)
   while res:
      ligne = res.group(1) + res.group(2)
      res = re.search("(.*)<[^>]+>(.*)",ligne)

   return ligne.replace("\r","").replace("\n","")

nbLettres = 0

for line in inputFile:
   if line != "\n":
      line.replace("\n"," \n")
   # Start of a new letter?
   res = re.search("^CDM(01|02|03|04|05|06|07|08|09|10)[a-b]*[-][0-9]+[.][a-e][.MmE]*", line)
   if res:
      # Save former letter
      letter["text"] = '<discours loc="CathMed" id="' + letter["id"] + '" date="' + letter["date"].replace(" ","").replace(".","").replace("\"","") + '"><p>' + letter["text"].replace("  "," ") + "</p></discours>"
      letters.append(letter)
      nbLettres += 1
      # Prepare next letter
      documentLineNb = 0
      letter = {}
      letter["id"] = nettoieLigne(line)
      letter["text"] = ""
      letter["date"] = ""
      letter["source"] = ""
      letter["destinataire"] = ""
   if documentLineNb == 1 and line != "\n" :
      letter["date"] = nettoieLigne(line).replace(".", "")
   if documentLineNb == 2 and line != "\n" :
      letter["source"] += " " + nettoieLigne(line)
   if documentLineNb == 3 and line != "\n" :
      letter["destinataire"] += " " + nettoieLigne(line)
   if documentLineNb < 4:
      # The line contains metadata about the letter
      if line != "\n" :
         if documentLineNb < 2 :
            documentLineNb += 1
      else:
         if documentLineNb == 2 and len(letter["source"]) > 0:
            documentLineNb = 3
         if documentLineNb == 3 and len(letter["destinataire"]) > 0:
            documentLineNb = 4
   else:
      # The line contains some text
      documentLineNb += 1
      if line == "\n":
         letter["text"] += "</p><p>"
      else:
         letter["text"] += " "
         previousEmptyLine = False
         letter["text"] += nettoieLigne(line)
         
letter["text"] = '<discours loc="CathMed" date="' + letter["date"].replace(" ","").replace(".","") + '"><p>' + letter["text"].replace("  "," ") + "</p></discours>"
letters.append(letter)
nbLettres += 1

print(str(nbLettres))

for letter in letters:
   if letter["id"] in letterIds:
      print(letter["id"])
      
      outputFileA.writelines("<article id='"+letter["id"]+"'><h2><!--Lettre n° "+letter["id"]+"-->"+ nettoieLigne(letter["date"]) + ", " + nettoieLigne(letter["destinataire"]) + "</h2>\n"
      + "<p><strong>Source :</strong> "+ nettoieLigne(letter["source"]) + "</p>\n<p>"
      + letter["text"].replace("<p></p>","").replace("<p","\n<p").replace("</discours>","\n</discours>").replace("<p>","  <p>")+"\n\n\n</article>")
      
      print("toto")

outputFileA.close()

print(nettoieLigne("<a>ooppoiipo</a>"))