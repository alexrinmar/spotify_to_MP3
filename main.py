import spotipy
import numpy as np
from spotipy.oauth2 import SpotifyOAuth
from pytubefix import Search
from pytubefix import YouTube
from pytube.innertube import _default_clients
from pytubefix import Playlist
import os

def download_spotify_music(spotify_playlist_url): # function to download  music from spotify playlist
    print('Processing Spotify Songs...')
    songs = sp.playlist_items(spotify_playlist_url,offset=0, # get list of songs
                                 fields='items,next,total',
                                 additional_types=('tracks', ))
    songs_in_playlist = [] # prime array for song titles that are in the spotify playlist
    for i, item in enumerate(songs['items']): # for each item in the playlist
        print('Processing Song {} of {} - {:.2f}%'.format(i+1,songs['total'],((i+1)/songs['total'])*100)) 
        track = item['track'] # get specific track
        info = [track['artists'][0]['name'],track['name']] # create title = track name + artist name
        info = ' '.join(info) # join strings
        # forbidden char correction for ffmpeg processing
        info_fmt = info.replace('(','') 
        info_fmt = info_fmt.replace(')','')
        info_fmt = info_fmt.replace('&','')
        info_fmt = info_fmt.replace(' ','_')
        info_fmt = info_fmt.replace("'",'_')
        songs_in_playlist.append(info_fmt+'.mp3') # append .mp3 to the formatted title
        print('Downloading {}...'.format(info))
        if os.path.isfile(sp_path+info_fmt+".mp3"): # if the file already exists
            print("FILE ALREADY DOWNLOADED - SKIPPING") # skip
        else:
            s = Search(info + ' lyrics') # search youtube for the song title and artist
            # 'lyrics' means you don't get weird 2000s music videos that are 2000 hours long
            yt = YouTube(str(s.videos[0].watch_url),# find the exact video
                     use_oauth=True,
                     allow_oauth_cache=True)
            audio = yt.streams.get_audio_only() # get audio only
            info_fmt_mp4 = info_fmt+".mp4" # create filename
            audio.download(output_path=sp_path,filename=str(info_fmt_mp4)) # download and name .mp4 file
            command = f"ffmpeg -hide_banner -loglevel error -y -i {sp_path+info_fmt_mp4} {sp_path+info_fmt}.mp3" # command to convert to .mp3
            os.system(command) # run command
            os.remove(sp_path+info_fmt_mp4) # remove .mp4 file
            print("Download Successful.") 
    print('All Spotify Songs Downloaded.') # when all songs have been downloaded
    songs_stored = os.listdir(sp_path) # songs_stored is a list of all of the songs in the device
    removed_songs = list(set(songs_stored)-set(songs_in_playlist)) # songs that are removed from spotify playlist
    for song in removed_songs: # for each song in this list
        print("Removing {}".format((song)))
        os.remove(sp_path+song) # remove the song
    

def download_youtube_music(youtube_playlist_url):
    i = 0
    songs_in_playlist = [] # prime array for song titles that are in the spotify playlist
    print('Processing YouTube Videos...')
    p = Playlist(youtube_playlist_url)
    for url in p.video_urls:
        yt = YouTube(url,# find the exact video
                use_oauth=True,
                allow_oauth_cache=True)
        audio = yt.streams.get_audio_only() # get audio only
        info = str(yt.title) # name of video on youtube from yt object i assume
        print('Processing Song {} of {} - {:.2f}%'.format(i+1,np.size(p.video_urls),((i+1)/np.size(p.video_urls))*100)) 
        info_fmt = info.replace('(','')  # formatted name of video on youtube
        info_fmt = info_fmt.replace(')','')
        info_fmt = info_fmt.replace('&','')
        info_fmt = info_fmt.replace(' ','_')
        info_fmt = info_fmt.replace("'",'_')
        songs_in_playlist.append(info_fmt+'.mp3') # append .mp3 to the formatted title
        info_fmt_mp4 = info_fmt+".mp4" # create filename
        print('Downloading {}...'.format(info))
        if os.path.isfile(yt_path+info_fmt+".mp3"): # if the file already exists
            print("FILE ALREADY DOWNLOADED - SKIPPING") # skip
        else:
            audio.download(output_path=yt_path,filename=str(info_fmt_mp4)) # download and name .mp4 file
            command = f"ffmpeg -hide_banner -loglevel error -y -i {yt_path+info_fmt_mp4} {yt_path+info_fmt}.mp3" # command to convert to .mp3
            os.system(command) # run command
            os.remove(yt_path+info_fmt_mp4) # remove .mp4 file
            print("Download Successful.") 
        i+=1
    print('All YouTube Songs Downloaded.') # when all songs have been downloaded
    songs_stored = os.listdir(yt_path) # songs_stored is a list of all of the songs in the device
    removed_songs = list(set(songs_stored)-set(songs_in_playlist)) # songs that are removed from spotify playlist
    for song in removed_songs: # for each song in this list
        print("Removing {}".format((song)))
        os.remove(yt_path+song) # remove the song
        

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="93e7428524534284ae4446ad070537ba",
                                               client_secret="d4b5cac6a28d4677ac2447117ff38cf7",
                                               redirect_uri="http://localhost:1234/",
                                               scope="user-library-read"))

_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

#path = '/home/alex/Github_Repos/spotify_to_MP3/Music_Test/'
sp_path = "/media/alex/SWIM_PRO/SpotifyMusic/"
yt_path = "/media/alex/SWIM_PRO/YoutubeMusic/"

spotify_playlist_url = 'https://open.spotify.com/playlist/6LZCc1li0I86SArPsDGObt'


youtube_playlist_url = 'https://www.youtube.com/playlist?list=PLcMVwU7ksM0J5J2UZXj1FecKzhigLbXFT'

download_spotify_music(spotify_playlist_url)
download_youtube_music(youtube_playlist_url)


