# Import customtkinter module
import io
import webbrowser
import json
import os
import base64
import requests
from requests import post, get
import json
import datetime
import urllib.request as urr
from urllib.request import urlopen as ur
import tkinter as tk
from array import *
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO
import customtkinter
from idlelib.tooltip import Hovertip
import customtkinter as ctk

# api info
client_id = '7883071c77ef487380197a2b9594176e'
client_secret = 'f11a9edc05c34ca8909e8e12b913312f'

# ctk.set_appearance_mode('dark')
# root = customtkinter.CTk()
# root.geometry("600x500")

app = ctk.CTk()
ctk.set_appearance_mode('dark')
app.geometry("750x650")
app.title("Hip Hop Artist Information")
app.resizable(False, False)

# Create a frame
frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40,
           fill='both', expand=True)

# create top welcome label
topLabel = ctk.CTkLabel(master=frame, text='T H E      R A P      S H E E T', font=("Arial", 34, 'bold'))
topLabel.place(relx=0.5, rely=0.03, anchor=N)

# create secondary label
secondary_label = ctk.CTkLabel(master=frame, text='Your Stop For Artist Information!', font=("Arial", 15, 'italic'))
secondary_label.place(relx=0.5, rely=0.11, anchor=N)

# create textbox for user input of artist name
searchEntry = ctk.CTkEntry(master=frame, width=250, corner_radius=25, border_width=1)
searchEntry.place(relx=0.5, rely=0.25, anchor=N)

def save_File_Display():
    dialog = ctk.CTkInputDialog(text="To save info to a file, enter a file name:", title="Saving Results")
    input = dialog.get_input()
    print(input)
    f = open(input + ".txt", "w")
    L = ["This is Delhi \n", "This is Paris \n", "This is London \n"]
    s = "Hello\n"

    # Writing a string to file
    f.write(s)

    # Writing multiple strings
    # at a time
    f.writelines(L)
    f.close()

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token


token = get_token()


def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}


album_list = []
release_list = []
headers = {
    'Authorization': 'Bearer {token}'.format(token=token)
}


def search_for_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print("No artist with that name exists")
        return None
    return json_result[0]


def get_songs_by_artist(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US'
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result


def get_albums_by_artist(token, id_album):
    url2 = f'https://api.spotify.com/v1/artists/{id_album}/albums/include_groups=album'
    headers = get_auth_header(token)
    result2 = get(url2, headers=headers)
    json_result = json.loads(result2.content)['name']
    json_result2 = json.loads(result2.content)['release_date']
    json_result3 = json.loads(result2.content)['album_type']
    print(json_result2)
    print(json_result3)
    return json_result


def show_results():
    # add music symbol image
    music_sybmol = ctk.CTkImage(light_image=Image.open('musicSymbol-removebg-preview.png'),
                                size=(30, 30))
    symbol_button = ctk.CTkButton(frame,
                                  image=music_sybmol,
                                  text="",
                                  fg_color='transparent',
                                  hover=False,
                                  command=open_Artist_Page)
    symbol_button.place(relx=0.7, rely=0.55, anchor=CENTER)
    symbol_tooltip = Hovertip(symbol_button, 'Open Artist Page')

    # popup to get file name for saving
    save_results_button = ctk.CTkButton(app, text="Save Results",
                           command=save_File_Display,
                           width=90,
                           height=30,
                           corner_radius=25)
    save_results_button.place(relx=0.5, rely=1, anchor=S)

    # get artist info needed for query
    artist = searchEntry.get()
    result = search_for_artist(token, artist)
    a_Name = result['name']
    artist_id = result['id']

    artist_Name_Label = ctk.CTkLabel(master=frame, text=a_Name, font=("Arial", 30, "bold"))
    artist_Name_Label.place(relx=0.5, rely=0.45, anchor=CENTER)

    BASE_URL = 'https://api.spotify.com/v1/'
    r = requests.get(BASE_URL + 'artists/' + artist_id + '/albums',
                     headers=headers,
                     params={'include_groups': 'album', 'limit': 3})
    d = r.json()

    for album in d['items']:
        print(album['name'], ' - ', album['release_date'])
        print(album['images'])
        album_list.append(album['name'] + "\n")
        release_list.append(album["release_date"])

    songs = get_songs_by_artist(token, artist_id)

    song_list = []

    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")
        song_list.append(song['name'] + "\n")

    # print(result['images'])

    top_songs_label = ctk.CTkLabel(master=frame, text=a_Name + "'s Top Tracks", font=("Arial", 20, "underline"))
    top_songs_label.place(relx=0.5, rely=0.55, anchor=CENTER)

    song1_label = ctk.CTkLabel(master=frame, text='1: ' + song_list[0]
                                                  + "2: " + song_list[1]
                                                  + "3: " + song_list[2]
                                                  + "4: " + song_list[3]
                                                  + "5: " + song_list[5], font=("Arial", 16))
    song1_label.place(relx=0.5, rely=0.67, anchor=CENTER)

    # get artist image
    url = result['images'][0]['url']
    re = requests.get(url)

    pilImage = Image.open(BytesIO(re.content))
    pilImage = pilImage.resize((100, 100), Image.ANTIALIAS)

    image = ImageTk.PhotoImage(pilImage)

    artistPicLabel = Label(image=image)
    artistPicLabel.image = image


    # get album art
    album1_url = album['images'][0]['url']
    re = requests.get(album1_url)
    pilImage = Image.open(BytesIO(re.content))
    pilImage = pilImage.resize((100, 100), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)

    # set and show album 1 label
    album1 = ctk.CTkLabel(master=frame, text=album_list[0], font=('Arial', 12))
    album1.place(relx=0.15, rely=0.92, anchor=CENTER)

    # set album 1 pic
    album1_img = ctk.CTkImage(light_image=Image.open('musicSymbol-removebg-preview.png'),
                                size=(30, 30))
    album1_img_button = ctk.CTkButton(frame,
                                  image=album1_img,
                                  text="",
                                  fg_color='transparent',
                                  hover=False,
                                  command=open_Artist_Page)
    album1_img_button.place(relx=0.15, rely=0.85, anchor=CENTER)

    # set album release date label
    album1_release_date = ctk.CTkLabel(master=frame, text=release_list[0], font=('Arial', 10))
    album1_release_date.place(relx=0.15, rely=0.95, anchor=CENTER)

    # set and show album 2 pic
    album2 = ctk.CTkLabel(master=frame, text=album_list[1], font=('Arial', 12))
    album2.place(relx=0.5, rely=0.92, anchor=CENTER)
    album2_img = ctk.CTkImage(light_image=Image.open('musicSymbol-removebg-preview.png'),
                              size=(30, 30))
    album2_img_button = ctk.CTkButton(frame,
                                      image=album2_img,
                                      text="",
                                      fg_color='transparent',
                                      hover=False,
                                      command=open_Artist_Page)
    album2_img_button.place(relx=0.5, rely=0.85, anchor=CENTER)

    # set album release date label
    album2_release_date = ctk.CTkLabel(master=frame, text=release_list[1], font=('Arial', 10))
    album2_release_date.place(relx=0.5, rely=0.95, anchor=CENTER)

    # set and show album 3 pic
    album3 = ctk.CTkLabel(master=frame, text=album_list[2], font=('Arial', 12))
    album3.place(relx=0.85, rely=0.92, anchor=CENTER)
    album3_img = ctk.CTkImage(light_image=Image.open('musicSymbol-removebg-preview.png'),
                              size=(30, 30))
    album3_img_button = ctk.CTkButton(frame,
                                      image=album3_img,
                                      text="",
                                      fg_color='transparent',
                                      hover=False,
                                      command=open_Artist_Page)
    album3_img_button.place(relx=0.85, rely=0.85, anchor=CENTER)

    # set album release date label
    album1_release_date = ctk.CTkLabel(master=frame, text=release_list[2], font=('Arial', 10))
    album1_release_date.place(relx=0.85, rely=0.95, anchor=CENTER)


# search label for search button
searchLabel = ctk.CTkLabel(master=frame, text='Artist Search', font=("Arial", 15))
searchLabel.place(relx=0.5, rely=0.19, anchor=N)

# create search button
searchButton = ctk.CTkButton(master=frame,
                             text='Search',
                             command=show_results,
                             corner_radius=25,
                             width=50)
searchButton.place(relx=0.5, rely=0.34, anchor=CENTER)

switch_var = ctk.StringVar(value="on")


def open_Artist_Page():
    artist = searchEntry.get()
    result = search_for_artist(token, artist)
    artist_id = result['id']
    new = 2
    webbrowser.open('https://open.spotify.com/artist/' + artist_id, new=new)


def switch_event():
    if switch_var.get() == 'off':
        ctk.set_appearance_mode('light')
    else:
        ctk.set_appearance_mode('dark')


def openWebsite():
    new = 2
    webbrowser.open('https://github.com/daltonpricee', new=new)


view_toggle = customtkinter.CTkSwitch(master=app, text="Light/Dark", command=switch_event,
                                      variable=switch_var, onvalue="on", offvalue="off")
view_toggle.place(relx=0.125, rely=0, anchor=N)

# add image next to top label
top_image = ctk.CTkImage(light_image=Image.open('logo2-removebg-preview.png'),
                         size=(50, 50))

top_logo_button = ctk.CTkButton(frame,
                                image=top_image,
                                text="",
                                width=50,
                                height=50,
                                fg_color='transparent',
                                hover=False,
                                command=openWebsite)
top_logo_button.place(relx=0.89, rely=0.015, anchor=N)
music_logo_tooltip = Hovertip(top_logo_button, 'Open Developer GitHub')

app.mainloop()
