#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ❯ SpotifyMediaCompiler - Created by sirnoob_1#0001 ❮ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

'''
   _____             _   _  __       __  __          _ _        _____                      _ _           
  / ____|           | | (_)/ _|     |  \/  |        | (_)      / ____|                    (_) |          
 | (___  _ __   ___ | |_ _| |_ _   _| \  / | ___  __| |_  __ _| |     ___  _ __ ___  _ __  _| | ___ _ __ 
  \___ \| '_ \ / _ \| __| |  _| | | | |\/| |/ _ \/ _` | |/ _` | |    / _ \| '_ ` _ \| '_ \| | |/ _ \ '__|
  ____) | |_) | (_) | |_| | | | |_| | |  | |  __/ (_| | | (_| | |___| (_) | | | | | | |_) | | |  __/ |   
 |_____/| .__/ \___/ \__|_|_|  \__, |_|  |_|\___|\__,_|_|\__,_|\_____\___/|_| |_| |_| .__/|_|_|\___|_|   
        | |                     __/ |                                               | |                  
        |_|                    |___/                                                |_|                  
'''

#━━━━━━━━━━━━━━━━━━━━━━━ ❯ SpotifyMediaCompiler Imports ❮ ━━━━━━━━━━━━━━━━━━━━━━━

#-Module Imports-
import spotipy
import requests
import time
import datetime

#-Class Imports-
from spotipy.oauth2 import SpotifyClientCredentials

#━━━━━━━━━━━━━━━━━━━━━ ❯ SpotifyMediaCompiler Declerations ❮ ━━━━━━━━━━━━━━━━━━━━━

#-Spotipy-
spotifyClient = spotipy.Spotify(
    client_credentials_manager = SpotifyClientCredentials( #- Head to developer.spotify.com and register API credentials
        client_id='CLIENTID',
        client_secret='CLIENTSECRET'
        )
    )

#-Variables-
responseList = []

#━━━━━━━━━━━━ ❯ Functions ❮ ━━━━━━━━━━━

#-Get_Api_Response-
def get_filtered_api_response(songArtist: str, songTitle: str) -> dict or list:

    #-Vars-
    badCharacters = ['(', ')', '\'', '&', '.']
    songTitleNew = ''
    strWordCounter = 0
    startTime = time.time()

    #-Sequence-

    for badChar in badCharacters: #- Iterating through the characters the API can't accept and removing them-

        if badChar == '&':
            songTitle = songTitle.replace('&', ', ')
            songArtist = songArtist.replace(' & ', ', ')
            continue

        songTitle = songTitle.replace(badChar, '')
        songArtist = songArtist.replace(badChar, '')

    for strWord in songTitle.split(' '):#- Checking for 'feat' - Karaoke results-

        if 'feat' in strWord.lower():
            break

        strWordCounter += 1

        if strWordCounter == 1:
            songTitleNew = strWord
            continue

        songTitleNew += ' ' + strWord

    songTitle = songTitleNew

    searchResults = spotifyClient.search( #- Searching the API-
        q = 'artist: ' + songArtist.lower()  + ' track:' + songTitle.lower(),
        type = 'track',
        limit = 1
    )


    finishTime = time.time() - startTime

    if searchResults['tracks']['items'] == []: #- Checking for a valid response, if it is a poor response this list is returned
        print(f'({datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}) [INFO] [GFAR] [FAILED] [{round(finishTime, 3)}s] Query ({songArtist} - {songTitle}) [RESPONSE] (Failed to locate song matching query)')

        return [songArtist, songTitle, 'https://i.imgur.com/h1bT9lD.png', None] #- returning failed prefixes. You can edit List[2] to a custom image to display

    else:
        print(f'({datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}) [INFO] [GFAR] [SUCCESS] [{round(finishTime, 3)}s] Query ({songArtist} - {songTitle}) [RESPONSE] (' + searchResults['tracks']['items'][0]['external_urls']['spotify'] + ')')

        return searchResults


#-Fill_Response_list-
def fill_response_list():
    global responseList

    #-Vars-
    tempList = [None, None, None, None, None, None]
    artistStr = ''
    artistStrCounter = 0
    songHistoryArtistStr = ''
    songHistoryCounter = 1
    songHistoryArtistStrCounter = 0
    startTime = time.time()


    #-Fetching SailorRadio API's Song Data-
    stationData = requests.get('STATION LINK')
    stationData = stationData.json()

    #-Searching Spotify API for song
    searchResultsNP = get_filtered_api_response(stationData['now_playing']['song']['artist'], stationData['now_playing']['song']['title'])

    if type(searchResultsNP) == dict:

        #-Formatting artists to be presented-
        for ResponseArtist in searchResultsNP['tracks']['items'][0]['artists']:

            if artistStrCounter == 0:
                artistStr += ResponseArtist['name']
                artistStrCounter += 1
            else:
                artistStr += ', ' + ResponseArtist['name']

        tempList[0] = [
            artistStr,
            searchResultsNP['tracks']['items'][0]['name'],
            searchResultsNP['tracks']['items'][0]['album']['images'][0]['url'],
            searchResultsNP['tracks']['items'][0]['external_urls']['spotify']
        ]

    else:
        tempList[0] = searchResultsNP


    for song in stationData['song_history']:
        searchResults = get_filtered_api_response(song['song']['artist'], song['song']['title'])
        songHistoryArtistStr = ''
        songHistoryArtistStrCounter = 0

        if type(searchResults) == dict:

            for songAuthor in searchResults['tracks']['items'][0]['artists']:

                if songHistoryArtistStrCounter == 0:
                    songHistoryArtistStr += songAuthor['name']
                    songHistoryArtistStrCounter += 1
                else:
                    songHistoryArtistStr += ', ' + songAuthor['name']
                songHistoryArtistStrCounter += 1

            tempList[songHistoryCounter] = [
                songHistoryArtistStr,
                searchResults['tracks']['items'][0]['name'],
                searchResults['tracks']['items'][0]['album']['images'][0]['url'],
                searchResults['tracks']['items'][0]['external_urls']['spotify']
            ]

        else:
            tempList[songHistoryCounter] = searchResults

        songHistoryCounter += 1
        time.sleep(0)

    finishTime = time.time() - startTime
    print(f'({datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}) [INFO] [FRL] [SUCCESS] [{round(finishTime, 3)}s] Filled ResponseList successfully')
    responseList = tempList

#-Update_Response_Data-
def update_response_data():
    global responseList


    if responseList == []: #- Checking if the responselist dict is empty, and filling it if it is

        fill_response_list()
        return

    #-Vars-
    tempList = [[]]
    fullList = responseList
    artistStr = ''
    artistStrCounter = 0
    iterCounter = 0
    startTime = time.time()

    #-Fetching SailorRadio API's Song Data-
    stationData = requests.get('STATIONLINK')
    stationData = stationData.json()

    #-Catching jingles-
    if 'JINGLE PREFIX'.lower() in stationData['now_playing']['song']['title'].lower():
        finishTime = time.time() - startTime
        return print(f'[INFO] [URD] [FAILED - NORMAL] [{round(finishTime, 3)}s] Jingle detected when calling update_response_data. Function returned')

    #-Searching Spotify API for song
    searchResultsNP = get_filtered_api_response(stationData['now_playing']['song']['artist'], stationData['now_playing']['song']['title'])

    if type(searchResultsNP) == dict:

        #-Formatting artists to be presented-
        for ResponseArtist in searchResultsNP['tracks']['items'][0]['artists']:

            if artistStrCounter == 0:
                artistStr += ResponseArtist['name']
                artistStrCounter += 1
            else:
                artistStr += ', ' + ResponseArtist['name']

        tempList[0] = [
            artistStr,
            searchResultsNP['tracks']['items'][0]['name'],
            searchResultsNP['tracks']['items'][0]['album']['images'][0]['url'],
            searchResultsNP['tracks']['items'][0]['external_urls']['spotify']
        ]

    else:
        tempList[0] = searchResultsNP

    if tempList[0] == responseList[0]:
        finishTime = time.time() - startTime
        print(f'({datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}) [INFO] [URD] [FAILED] [{round(finishTime, 3)}s] Failed to update ResponseList due to the current song matching')

        return


    for item in fullList:

        tempList.append(item)

        iterCounter +=1
        if iterCounter == 6:
            break

    finishTime = time.time() - startTime
    responseList = tempList

    print(f'({datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")}) [INFO] [URD] [SUCCESS] [{round(finishTime, 3)}s] Updated ResponseList succesfully')
    return(responseList)

update_response_data()

'''
Call update_response_data() to automatically update the 'cache' and updates in the future. The function handles
jingles and maintains the old list when azura updates the nowplaying. Run constantly to maintain data.
'''
