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
from lib2to3.pgen2 import token
import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
import os
load_dotenv()

#spotify
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



#youtube
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

yt_secret_key = os.getenv('yt_client_secret')
yt_access_token = ""
yt_refresh_token = os.getenv('yt_refresh')
overallState = ''
overallCredentials = ''

#youtube
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES, redirect_uri = 'https://www.youtube.com/')
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def insertIntoPlaylist(videoId, playListTOAdd):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": f'{playListTOAdd}',
            "resourceId": {
              "kind": "youtube#video",
              "videoId": f'{videoId}'
            }
          }
        }
    )
    response = request.execute()

def searchYoutube(query):
    request = youtube.search().list(
        part="snippet",
        q=query
    )
    response = request.execute()
    toPrint = response["items"][0]["snippet"]["title"]
    toReturn = response["items"][0]["id"]["videoId"]
    return toReturn


def createNewPlaylist(name):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": f'{name}',
            "description": "Spotify playlist",
            "defaultLanguage": "en"
          },
          "status": {
            "privacyStatus": "private"
          }
        }
    )
    response = request.execute()
    return response["id"]



#spotify 
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


def user_Playlists(id,limit=10):
    SPOTIFY_URL = 'https://api.spotify.com/v1/users/'+id+'/playlists?limit=' + str(limit)
    response = requests.get(SPOTIFY_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        })
    json_resp = response.json()
    toPrint =""
    toReturn = [0]
    toReturPlayListNames = [0]
    counter = 1
    for obj in json_resp["items"]:
        toPrint += str(counter) + ". " + obj["name"] + "\n"
        toReturn.append(obj["id"])
        toReturPlayListNames.append(obj["name"])
        counter+=1
    print(toPrint)
    return toReturn,toReturPlayListNames

def getPlayListItems(id):
    SPOTIFY_URL = 'https://api.spotify.com/v1/playlists/'+id+'/tracks?fields=items(track(name%2Cartists(name)))'
    response = requests.get(SPOTIFY_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        })
    json_resp = response.json()
    songToReturn = []
    artistToReturn = []
    for obj in json_resp["items"]:
        songToReturn.append(obj["track"]["name"])
        artistToReturn.append(obj["track"]["artists"][0])
    return songToReturn,artistToReturn

def main():
    getNewAccessToken()
    print()
    print()
    userPlaylists, userPlayListNames = user_Playlists('anguyen22030',10)
    playlistToConvert= input("Select the playlist you wish to convert by entering the number next to the playlist name ")
    playListSongs,playListArtists = getPlayListItems(userPlaylists[int(playlistToConvert)])
    playlistId = createNewPlaylist(userPlayListNames[int(playlistToConvert)] + " from spotify")
    counter = 0
    for obj in playListSongs:
        addToPlaylist = searchYoutube(obj + " " + playListArtists[counter]['name'])
        insertIntoPlaylist(addToPlaylist, playlistId)
        counter+=1
    print("Done!")
    # Get credentials and create an API client

if __name__ == '__main__':
    main()