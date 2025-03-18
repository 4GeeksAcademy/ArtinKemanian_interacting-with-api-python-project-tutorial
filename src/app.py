import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# load the .env file variables
load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

conn = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret))

id_artista = "7wHbsRbx23UPiHo7sNoXEb"

response = conn.artist_top_tracks(id_artista)
if response:
    pistas = response["tracks"]
    pistas = [{k: (v/(1000*60))%60 if k == "duration_ms" else v for k, 
               v in pista.items() if k in ["name", "popularity", "duration_ms"]} for pista in pistas]

df_pistas = pd.DataFrame.from_records(pistas)
df_pistas.sort_values(["popularity"], inplace = True)

print(df_pistas.head(3))

scatter_plot = sns.scatterplot(data = df_pistas, x = "popularity", y = "duration_ms")
fig = scatter_plot.get_figure()
fig.savefig("scatter_plot.png")