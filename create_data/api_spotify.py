from requests import post, get
import os
import base64
import json

client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {auth_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {'grant_type': 'client_credentials'}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

def search_for_twitty(token, artist_id):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    headers = get_auth_header(token)

    request = get(url, headers=headers)
    response = request.json()
    albums = response['items']

    twitty_info = []

    for album in albums:
        album_id = album['id']
        url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
        headers = get_auth_header(token)

        request = get(url, headers=headers)
        response = request.json()
        tracks = response['items']

        for track in tracks:
            track_info = {
                "track_id": track['id'],
                "track_name": track["name"],
                "duration_ms": track["duration_ms"],
                'album_name': album['name'],
                'release_date': album['release_date'],
            }

            twitty_info.append(track_info)

    return twitty_info


def main():
    token = get_token()
    twitty = search_for_twitty(token, '7gi3jmwpUpNWdswT8eEprF')
    with open('conway_info.json', 'w') as json_file:
        json.dump(twitty, json_file, indent=4)

if __name__ == '__main__':
    main()