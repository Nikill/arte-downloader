import urllib.request, json,sys, requests, urllib3
import pandas as pd
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
while True:
    try:
        video = input("URL de la vidéo ? (Arte / M6 Video Bank) > ").strip()
    except ValueError:
        print("La référence doit être un nombre ( ex.: 296638 ).")
        continue
    else:
        break
if "m6" in str(video.split('/')[2]):
    print("Ce programme permet de récupérer les URL directes des vidéos de m6videobank.com\n"
              "Attention : l'utilisation abusive peut vous faire IP Ban du service.\n"
              "En cas de problème ou pour plus d'infos, me faire signe sur le Discord :).\n"
              "- PV\n")
    print(" - Programme M6 Video Bank - ")
    video_id = video.split('/')[6]
    serveurs = {
            "zooms": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "zooms2": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
            "zooms3": [10, 11, 12, 13, 14]
            }
    for zoom, dossier in serveurs.items():
        for ref in dossier:
            url = f"https://www.m6videobank.com/{zoom}/{str(ref).zfill(11)}/{video}.h264"
            resultat = requests.head(url, verify=False).status_code
            if resultat != 404:
                print(f"Vidéo retrouvée : {url}")
                kill = input("Appuyer sur Entrée pour fermer le programme.")
                sys.exit(0)
elif "arte" in str(video.split('/')[2]):
    video_id = video.split('/')[5]
    text_url = """https://api.arte.tv/api/player/v1/config/fr/""" + video_id
    print("- Programme ARTE - ")
    fields = ['id','quality','width','height', 'mediaType','mimeType', 'bitrate', 'url', 'versionProg','versionCode', 'versionLibelle', 'versionShortLibelle']
    wjdata = json.load(urllib.request.urlopen(text_url))
    print("video being processed : " + wjdata['videoJsonPlayer']["eStat"]["streamName"] + " | Original Language : " + wjdata['videoJsonPlayer']["language"])
    df = pd.DataFrame([],  columns =  ['id','quality','width','height', 'mediaType','mimeType', 'bitrate', 'url', 'versionProg','versionCode', 'versionLibelle', 'versionShortLibelle'])
    for qual in wjdata['videoJsonPlayer']['VSR']:
        row_to_add = pd.DataFrame({'id':[wjdata['videoJsonPlayer']['VSR'][qual]['id']],'quality':wjdata['videoJsonPlayer']['VSR'][qual]['quality'],'width':wjdata['videoJsonPlayer']['VSR'][qual]['width'],'height':wjdata['videoJsonPlayer']['VSR'][qual]['height'], 'mediaType':wjdata['videoJsonPlayer']['VSR'][qual]['mediaType'],'mimeType':wjdata['videoJsonPlayer']['VSR'][qual]['mimeType'], 'bitrate':wjdata['videoJsonPlayer']['VSR'][qual]['bitrate'], 'url':wjdata['videoJsonPlayer']['VSR'][qual]['url'], 'versionProg':wjdata['videoJsonPlayer']['VSR'][qual]['versionProg'],'versionCode':wjdata['videoJsonPlayer']['VSR'][qual]['versionCode'], 'versionLibelle':wjdata['videoJsonPlayer']['VSR'][qual]['versionLibelle'], 'versionShortLibelle':wjdata['videoJsonPlayer']['VSR'][qual]['versionShortLibelle']})
        df = df.append(row_to_add,ignore_index=True)
    df["ShortDescription"]= wjdata['videoJsonPlayer']["V7T"]
    #df["LongDescription"] = wjdata['videoJsonPlayer']["VDE"]
    df["Category"] = wjdata['videoJsonPlayer']["category"]["name"]
    df["OriginalLanguage"] = wjdata['videoJsonPlayer']["language"]
    df["Title"] = wjdata['videoJsonPlayer']["eStat"]["streamName"]
    df['height'] = pd.to_numeric(df['height'])
    df['width'] = pd.to_numeric(df['width'])
    df['bitrate'] = pd.to_numeric(df['bitrate'])
    df['versionProg'] = pd.to_numeric(df['versionProg'])
    df_hq = df.loc[(df['height']>=720) & (df["mediaType"] == 'mp4')]
    list_of_versions = df_hq[['versionShortLibelle','height']].rename(columns = {'height':'Quality'})
    print("Versions available : \n")
    print(list_of_versions)
    version = input('Please Enter Your Version Name (VO / VF / ...) \n')
    url = df_hq['url'].loc[df_hq['versionShortLibelle'] == version]
    url = url.values[0]
    print("here is your download link : " + url)
    kill = input("Appuyer sur Entrée pour fermer le programme.")
    sys.exit(0)
else:
    print("URL invalide")
