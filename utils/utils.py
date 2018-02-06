def write_list_of_dictionaries_to_file(data, filename, mode=None):
    """
    input - list of dictionaries as data, filename to be written to
    output - none, out file.
    """
    import unicodecsv as csv

    keys = data[0].keys()

    if mode:
        with open(filename, mode) as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
    else:
        with open(filename, "wb") as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)


def read_csv_to_list_of_dictionaries(filename):
    """
    input - list of dictionaries as data, filename to be read from
    output - list of dictionaries
    """
    import unicodecsv as csv

    data = []

    with open(filename, "rb") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    return data


def make_corrections(filename, correction_filename):
    """
    reads in a filename and a correction file name,
    searches for entries with a spotify id but no other spotify features,
    then sets the features using the id and updates the file
    """
    from spotify_utils import create_auth, set_track_data, set_album_data, set_artist_data, set_audio_features

    corrections = read_csv_to_list_of_dictionaries(correction_filename)
    correction_lookup = dict((er['title'], er['track_id'])
                             for er in corrections)

    data = read_csv_to_list_of_dictionaries(filename)

    sp = create_auth()

    for song in data:
        if song['title'] in correction_lookup and correction_lookup[song['title']]:
            song['track_id'] = correction_lookup[song['title']].split(":")[2]
            set_track_data(song, sp)
            set_album_data(song, sp)
            set_artist_data(song, sp)
            set_audio_features(song, sp)
            print "Updated {} by {}".format(song['title'], song['artist'])

    write_list_of_dictionaries_to_file(data, filename=filename)


def set_timedelta(song):
    """
    Converts album release dates to datetime and computes the timedelta
    """
    from dateutil import parser
    from datetime import datetime
    # convert now and album release to date time
    if 'now_release_date' in song.keys() and not isinstance(song['now_release_date'], datetime):
        now_date = song['now_release_date']
        if ";" in now_date:
            now_date = now_date.split(";")[0]
        song['now_release_date'] = parser.parse(now_date)
    if 'album_release_date' in song.keys() and song['album_release_date'] and not isinstance(song['album_release_date'], datetime):
        song['album_release_date'] = parser.parse(song['album_release_date'])
    # find time delta by subtracting, taking day, and int casting
    if isinstance(song['album_release_date'], datetime) and isinstance(song['now_release_date'], datetime):
        song['timedelta'] = int(
            (song['now_release_date'] - song['album_release_date']).days)


def filter_dataframe_by_year(dataframe, field, year):
    """
    input - dataframe, field with dates, year (inclusive)
    output - data frame with data from the input year and forward
    """
    import pandas as pd

    def year_filter(y):
        return int(y[:4])

    return dataframe.loc[dataframe[field].apply(year_filter) >= year]


def make_predictions(dataframe, model, feature_list):
    """
    input - dataframe, classifier
    output - list of tuples with artist, title, confidence in prediction
    """
    next_album = []
    for i, song in dataframe.iterrows():
        # filter our features, make a prediction
        x = [song[f] for f in feature_list]
        res = model.predict_proba(x)[0]
        # if there is a higher probability of the label being 1 (indicating
        # now-ness), append to our album
        if res[1] > res[0]:
            next_album.append((song['artist'], song['title'], res[1]))
    # sort album on prediction confidence and return top 20
    return sorted(next_album, key=lambda x: x[2], reverse=True)[:20]
