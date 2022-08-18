from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

client_id = ''
client_sec = ''

data_user = input("Escolha o dia que deseja voltar no tempo e rankear as musicas: \n [Ex: Ano-dia-mês = 1989-07-11] Agora você: ")
responde = requests.get(f"https://www.billboard.com/charts/hot-100/{data_user}/")
yc_web_page = responde.text
soup = BeautifulSoup(yc_web_page, "html.parser")
# sounds = soup.findAll(name="h3", class_="c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet")
sounds = soup.find_all(name='h3', class_="a-no-trucate")
music_names = [sound.getText().strip() for sound in sounds]
# print('\n' .join(music_names))

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_sec,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]

song_uris = []
year = data_user.split("-")[0]
for song in music_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#criar lista no spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{data_user} Billboard 100", public=False)
print(playlist)

#adicionar sons encontrados a playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
