def create_auth():
    """
    Authorizes w/ Spotify
    """
    import sys
    import os
    import spotipy
    from spotipy import util

    os.environ["SPOTIPY_CLIENT_ID"] = '7e4f1f9e4f9342429ea79c0c3ade3284'
    os.environ["SPOTIPY_CLIENT_SECRET"] = ""  # fill in with your secret
    os.environ["SPOTIPY_REDIRECT_URI"] = 'http://localhost/'

    # Authenticating for Spotify
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Usage: %s username" % (sys.argv[0],)
        sys.exit()

    scope = "user-library-read"
    token = util.prompt_for_user_token(username, scope)

    if token:
        return spotipy.Spotify(auth=token)
    else:
        print "Can't get token for", username


def set_spotify_data(song, sp):
    """
    input - list of song dictionaries with spotifyID
    output - none. void method that sets audio features
    """
    import unicodecsv as csv

    # Adding features for each song
    # Taylor Swift has famously removed here music from Spotify so we can
    # skip her here
    t_swift = "Taylor Swift"
    if song['artist'] == t_swift or t_swift in song['artist']:
        return
    # Running all the Spotify queries necessary to satisfy our model
    try:
        set_spotify_id(song, sp)
        set_track_data(song, sp)
        set_album_data(song, sp)
        set_artist_data(song, sp)
        set_audio_features(song, sp)
    except:
        # If song cannot be found, write its title and artist to a file for
        # searching later
        print "Can't find: " + song['title']
        with open("corrections.csv", "ab") as file:
            fields = ['title', 'artist', 'track_id']
            writer = csv.DictWriter(file, fields)
            writer.writerow(
                {"title": song['title'], "artist": song['artist'], "track_id": None})


def set_spotify_id(song, spotipy_instance):
    """
    input - song and spotify instance
    output - sets corresponding spotify id
    """
    artist = song['artist']

    if isinstance(artist, list):
        artist = artist[0]

    q = "title:{} artist:{}".format(
        song['title'].encode('utf-8'), artist.encode('utf-8'))
    result = spotipy_instance.search(q)['tracks']['items'][0]
    song['track_id'] = result['id']


def set_artist_data(song, spotipy_instance):
    """
    input - song dictionary and spotipy instance
    output - none, void. sets artist popularity
    """
    result = spotipy_instance.artist(song['artist_id'])
    song['artist_popularity'] = result['popularity']


def set_audio_features(song, spotipy_instance):
    """
    input - song dictionary and spotipy instance
    output - none, void. sets audio_features
    """
    result = spotipy_instance.audio_features(str(song['track_id']))[0]
    for k, v in result.iteritems():
        song[k] = v


def set_album_data(song, spotipy_instance):
    """
    input - song dictionary and spotipy instance
    output - none, void. sets album popularity
    """
    result = spotipy_instance.album(song['album_id'])
    song['album_popularity'] = result['popularity']
    song['album_release_date'] = result["release_date"]


def set_track_data(song, spotipy_instance):
    """
    input - song dictionary and spotipy instance
    output - none, void. sets track features
    """
    result = spotipy_instance.track(song['track_id'])
    song['album_id'] = result['album']['id']
    song['track_popularity'] = result['popularity']
    song['album_name'] = result['album']['name']
    song['artist'] = result['artists'][0]['name']
    song['artist_id'] = result['artists'][0]['id']
    song['title'] = result['name']
