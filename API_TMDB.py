# importeer de nodige modules
import requests
import json
import sys
from requests.structures import CaseInsensitiveDict     # gebruik van bearer token
from tabulate import tabulate                           # maak table overzichtelijk

# Variabelen declareren
search = ""
teller = 1
while (search == ""):                                   # geen lege query uitvoeren
    search = input(str("Welke film wilt u zoeken? (Typ q of quit om te stoppen) "))
    if search == "q" or search == "quit":               # mogelijkheid voor vroegtijdig te stoppen
        sys.exit()

# authentication m.b.v. bearer token (APIv4 Read Access Token)
bearer = input(str("Vul hier uw Bearer token in: "))
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer "+bearer

# programma uitvoeren
while True:
    url = "https://api.themoviedb.org/3/search/movie?query="+search+"&page="+str(teller)    # url aanmaken
    response = requests.get(url, headers=headers)                                           # data ophalen
    content = json.loads(response.content)                                                  # data decoden
    output = []                                                                             # list aanmaken
    header = ["Title", "Release Date", "Rating"]
    output.append(header)
    for movie in content["results"]:                                                        # lijst opvullen per gevonden zoekresultaat
        this = [movie["title"],movie["release_date"],movie["vote_average"]]
        output.append(this)

    if content["page"] > content["total_pages"]:
        print("\n"+"Er zijn geen zoekresultaten beschikbaar voor uw zoekopdracht.")
        sys.exit()
    
    # nodige prints uitvoeren
    print("\n"+"STATUS CODE: "+str(response.status_code)+"\n")
    print(tabulate(output, headers="firstrow", tablefmt="fancy_grid"))

    # meerdere paginas
    if content["page"] == content["total_pages"]:
        print("\n"+"Dit zijn alle films die voldoen aan uw zoekopdracht."+"\n")          # wanneer alle films getoond zijn
        sys.exit()
    else:
        print("\n"+"Er zijn nog meer zoekresultaten.")        # wanneer er nog meer zoekresultaten beschikbaar zijn op een volgende pagina
        yesno = input("Wilt u deze bekijken? Typ Y (ja) of N (nee): ")
        if yesno == "N" or yesno == "n" or yesno == "nee":
            sys.exit()
        else:
            teller += 1