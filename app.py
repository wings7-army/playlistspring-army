from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ACCESS_TOKEN = 'BQC8O1Os_e-9hQsA2NxexNCmurpEdtTtXbR4qPBZUidAfktWbEJOva2ZpszChGbwp4Hrc2mefAYIFpYu6DIz9B6KWmmtaoiXkD_h8BCWLlon2A0kzW7GLdfBX_9Jqc5z3f'
USER_ID = '31fxdva2g6awztsxw2wk4ypcitye'

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

    tracks = uris * min(cantidad, 100)
    requests.post(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers,
        json={"uris": tracks}
    )

    return jsonify({"playlist_url": playlist.get("external_urls", {}).get("spotify", "")})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
