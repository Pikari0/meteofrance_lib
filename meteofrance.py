import requests
import re


def recherche_ville(texte):
    r = requests.get("http://www.meteofrance.com/mf3-rpc-portlet/rest/lieu/facet/previsions/search/"+texte)
    premier_resultat = r.json()[0]
    code_lieu = "/"+premier_resultat['slug']+"/"+premier_resultat['codePostal']
    return {"code":code_lieu,"nom":premier_resultat['nomAffiche']}

def previsions(ville):
    lieu=ville['code']
    r = requests.get("http://www.meteofrance.com/previsions-meteo-france"+lieu)

    retour = {'ville':ville['nom'],'previsions':[]}

    page = r.text
    
    # on extrait les prévisions par jours
    parties=page.split('prevision-horaire')

    # parties[0] -> jours de la semaine
    # parties[>0] -> par heure    


    #### à récupérer 
    # le libellé de la météo
    # la température
    # ressenti
    # UV
    # vent	
    ## c'est dans <ul class="day-data">
    
    aujourdhui = parties[1]
    heures = aujourdhui.split('<button class="time-range-trigger">')    

    for heure in heures[1:]:
        jour = re.search(r'<h3>([A-zÀ-ÿ0-9]|\s)*',heure).group(0).replace("<h3>",'')
        horaire = re.search(r'<time datetime="[0-9]*h',heure).group(0).replace('<time datetime="','')
        meteo = re.search(r'<li class="day-summary-label">([A-zÀ-ÿ0-9]|\s)*',heure).group(0).replace('<li class="day-summary-label"> ','')
        temperature = re.search(r'<li class="day-summary-temperature"> [0-9]*°C',heure).group(0).replace('<li class="day-summary-temperature"> ','')
        ressenti = re.search(r'Ressenti</abbr> [0-9]*°C',heure).group(0).replace('Ressenti</abbr> ','')
        vent = re.search(r'[0-9]* km\/h',heure).group(0).replace('</span>','')
        uv = re.search(r'<li class="day-summary-uv">UV [0-9]*',heure).group(0).replace('<li class="day-summary-uv">','')

        tab = {'jour':jour,'horaire':horaire,'meteo':meteo,'temperature':temperature,'ressenti':ressenti,'vent':vent,'uv':uv}
        retour['previsions'].append(tab)
    return retour

print(previsions(recherche_ville("lyon")))
