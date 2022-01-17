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
ACCESS_TOKEN =''
SPOTIPY_CLIENT_ID = 'e13faa7573d7435998090c6718e11728'
SPOTIPY_CLIENT_SECRET  = '717c2dc20cc64b71a048a7b97a8c9a4e'

scope  = 'user-library-read user-read-private playlist-modify-private playlist-read-private'
code = 'AQC5HW4zeJLM2RUr23ohtofLmOOhu2exCKB929mruVx2nTt5SKmQHoZU12vm0AYRTG7_3Xa0tmw1y6c1nBoBeuycbLxBV5Bddl_bIixoAzIR242IN7oauKq04LSejykOo_vgKQBsIwIKE6Ya2B2Bz5UQ5-8ACY6yIZr5739zAuC_p7O152X-_QjcxktvdwqhdPyAbrP0qHAoTcunBD3aykLvYXcDz1bQYqBuH_WG6lZuIbUR7xx1GvRlaVIbhJBX1rMKU9X02jSWGcvWAU38BEY5RLvKfjPGT0UezbqivxSCcVHPmJbh'
refresh_token = 'AQCuCRXMlaK6p8YDoXMImA6wzorTbune619zysFPYvCsC2dCoY-OLkQM--iSRfzxsu4GvH8eM0bZ5AUS9wcZ1DHdRuvmtTanyopHTNIQ6R8X2J_sF_NysiimtzHoSEPjUPQ'
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
    token = util.prompt_for_user_token(username,scope,client_id='e13faa7573d7435998090c6718e11728',client_secret='717c2dc20cc64b71a048a7b97a8c9a4e',redirect_uri='https://open.spotify.com/collection/playlists')
    if token:
        ACCESS_TOKEN = token
    else:
        print("Can't get token for", username)

def getRefreshToken():
    SPOTIFY_URL = TOKEN_URL
    autho_ascii = SPOTIPY_CLIENT_ID +":" + SPOTIPY_CLIENT_SECRET
    autho_bytes = autho_ascii.encode('ascii')
    base64_bytes = base64.b64encode(autho_bytes)
    base64_message = base64_bytes.decode('ascii')
    print(base64_message)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Authorization": 'Basic ZTEzZmFhNzU3M2Q3NDM1OTk4MDkwYzY3MThlMTE3Mjg6NzE3YzJkYzIwY2M2NGI3MWEwNDhhN2I5N2E4YzlhNGU='
    }
    data={
        "grant_type": 'authorization_code',
        "code": 'AQDLaD1L_IHhQkmgRy6I-eEEO1y1w8D6u5CVCsYndQKfaOBcHfO9CETTURZTkZxQGxo9jo5IZ5qDQVSe2sCqM5ZL4C-SqoYvABISGtSk08FXdOOQq5cJ5DqIJmo_OkpVHZEnX1iwz4Xj6Mrud8qOd2cjQW0u97SlNk0QWX6exE3kIvj0ZxSIiyszDF0wfaP-wbNA55VjLTXZ-xgZIbS-fJeywukEuHqaQFYpvEyU72ezXubDRRgp-7zdOzZXyXY7wZzaJejuN61As08ILkYm62aBld7t5aATusIh3AO7TvTo-sT-LBJR',
        "redirect_uri": 'https://open.spotify.com/collection/playlists',
        }
    
    response = requests.post(SPOTIFY_URL, headers=headers, data=data) 
    print(response.json())
def getNewAccessToken():
    global ACCESS_TOKEN
    SPOTIFY_URL = TOKEN_URL
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "Authorization": 'Basic ZTEzZmFhNzU3M2Q3NDM1OTk4MDkwYzY3MThlMTE3Mjg6NzE3YzJkYzIwY2M2NGI3MWEwNDhhN2I5N2E4YzlhNGU='
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