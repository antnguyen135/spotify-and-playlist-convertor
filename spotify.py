import json
import requests
import urllib.parse
from urllib.parse import urlencode
import base64
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import spotipy
import spotipy.util as util
from dotenv import load_dotenv
import os
load_dotenv()

ACCESS_TOKEN =''
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET  = os.getenv("SPOTIPY_CLIENT_SECRET")
autho_ascii = str(SPOTIPY_CLIENT_ID) +":" + str(SPOTIPY_CLIENT_SECRET)
autho_bytes = autho_ascii.encode('ascii')
base64_bytes = base64.b64encode(autho_bytes)
base64_message = base64_bytes.decode('ascii')
scope  = 'user-library-read user-read-private playlist-modify-private playlist-read-private'
code = os.getenv("code")
refresh_token = os.getenv("refresh_token")
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'
def create_playlist(name,public):
    SPOTIFY_URL = 'https://api.spotify.com/v1/users/anguyen22030/playlists'
    
    response = requests.post(SPOTIFY_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        },
        json={
            "name": name,
            "public": public
        })    
    json_resp = response.json()
    return json_resp

def getToken(username):
    global ACCESS_TOKEN
    scope  = 'user-library-read user-read-private playlist-modify-private playlist-read-private'
    token = util.prompt_for_user_token(username,scope,client_id={SPOTIPY_CLIENT_ID},client_secret={SPOTIPY_CLIENT_SECRET},redirect_uri='https://open.spotify.com/collection/playlists')
    if token:
        ACCESS_TOKEN = token
    else:
        print("Can't get token for", username)

def getRefreshToken():
    SPOTIFY_URL = TOKEN_URL
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Authorization": f'Basic {base64_message}'
    }
    data={
        "grant_type": 'authorization_code',
        "code": f'{code}',
        "redirect_uri": 'https://open.spotify.com/collection/playlists',
        }
    
    response = requests.post(SPOTIFY_URL, headers=headers, data=data) 
    print(response.json())
def getNewAccessToken():
    global ACCESS_TOKEN
    SPOTIFY_URL = TOKEN_URL
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Authorization": f'Basic {base64_message}'
    }
    data={
        "grant_type": 'refresh_token',
        "refresh_token": refresh_token,
        }
    response = requests.post(SPOTIFY_URL, headers=headers, data=data)
    ACCESS_TOKEN = response.json()["access_token"]
def Arist_topTracks(id,market="US"):
    SPOTIFY_URL = 'https://api.spotify.com/v1/artists/' + id + '/top-tracks?market=' + market
    response = requests.get(SPOTIFY_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        })
    json_resp = response.json()
    toReturn =""
    outF = open("output.txt", "a")
    n = 0
    for obj in json_resp["tracks"]:
        outF.write(str(n) +': ' + obj["name"] + "   id: " + obj["id"] + "\n")
        toReturn += obj["name"] +"\n"
        add = input("Would you like to add " + obj["name"]+ " to your playlist? (yes or no) ")
        print()
        if(add.lower() =="yes"):
            addSong("6ww7Bdls8NuMmdoivCBYX5", obj["uri"],0)
        n +=1
    outF.close()
    return toReturn

def deleteSong(playlistID,songURI):
    
    return "yes"

def user_Playlists(id,limit=10):
    SPOTIFY_URL = 'https://api.spotify.com/v1/users/'+id+'/playlists?limit=' + str(limit)
    response = requests.get(SPOTIFY_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        })
    json_resp = response.json()
    toReturn =""
    outF = open("output.txt", "a")
    outF.write('\nMy Playlists:\n')
    for obj in json_resp["items"]:
        outF.write('name: ' + obj["name"] + "   id: " + obj["id"] + "\n")
        toReturn += obj["name"] +"\n"
    outF.close()
    return toReturn

def addSong(playListID,songuri,position=0):
    SPOTIFY_URL = 'https://api.spotify.com/v1/playlists/' + playListID + '/tracks?position=' +str(position) + '&uris=' + songuri
    response = requests.post(SPOTIFY_URL,
    headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        })
    return "done"

def search_Artist(name,typeE,market,limit=1):
    SPOTIFY_URL = 'https://api.spotify.com/v1/search?q=' + name + '&type=' + typeE + '&market=' + market + '&limit=' + str(limit)
    response = requests.get(SPOTIFY_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        })

    json_resp = response.json()
    with open("fullJson.json", "w") as outfile:
        outfile.write(json.dumps(json_resp))
    return json_resp["artists"]["items"][0]["external_urls"]["spotify"],json_resp["artists"]["items"][0]["id"]

def main():
    #playlist = create_playlist(name="GO ANTHONY!", public=False)
    #print('token:' + ACCESS_TOKEN)
    #username = input("Enter username: ")
    #getToken(username)
    getNewAccessToken()
    #print(f'token: {ACCESS_TOKEN}')
    artistName = input('Enter an artist Name: ')
    search,artistID = search_Artist(urllib.parse.quote(artistName),"artist","US")
    outF = open("output.txt", "w")
    outF.write('URL: ' + search + "\n")
    outF.write('ID: ' + artistID + "\n\n")
    outF.write('TOP TRACKS:\n')
    outF.close()
    topTracks = Arist_topTracks(artistID)
    userPlaylists = user_Playlists('anguyen22030',10)
    
    #print(f"Playlist: {playlist}")
    #print(f"Search: {search}")
    #print(topTracks)

    
if __name__ == '__main__':
    main()