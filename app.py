from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
USER_ID = os.environ.get('USER_ID')

@app.route('/crear_playlist', methods=['POST'])
def crear_playlist():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion', '')
    cantidad = int(data.get('cantidad', 1))
    uris = data.get('uris', [])

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Crear la playlist
    response = requests.post(
        f"https://api.spotify.com/v1/users/{USER_ID}/playlists",
        headers=headers,
        json={
            "name": nombre,
            "description": descripcion,
            "public": True
        }
    )

    playlist = response.json()
    playlist_id = playlist.get("id")

    # Agregar canciones
    tracks = uris * min(cantidad, 100)
    requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        json={"uris": tracks}
    )

    return jsonify({
        "playlist_url": playlist.get("external_urls", {}).get("spotify", ""),
        "playlist_id": playlist_id
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
