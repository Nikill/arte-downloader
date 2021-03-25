import urllib.request, json
import pandas as pd
from IPython.core.display import display

def arte_downloader(total_url):
    video_id = total_url.split('/')[5]
    text_url = """https://api.arte.tv/api/player/v1/config/fr/""" + video_id
    print("URL being processed is : " + text_url)
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
    list_of_versions = df_hq['versionShortLibelle']
    print("Version available : \n")
    display(list_of_versions)
    version = input('Please Enter Your Version \n')
    url = df_hq['url'].loc[df_hq['versionShortLibelle'] == version]
    url = url.values[0]
    print("here is your download link" + url)
