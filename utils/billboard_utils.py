def scrape_billboard(number_of_weeks):
    """
    input - number of weeks to scrape into the past
    output - dictionary with spotify id as key, value is dictionary with title
        and artist values
    """
    from spotify_utils import create_auth, set_track_data, set_album_data, set_artist_data, set_audio_features
    from utils import write_list_of_dictionaries_to_file
    import billboard
    import Tkinter

    chart = billboard.ChartData(name='hot-100')
    data = []
    id_list = []
    count = 0
    sp = create_auth()

    while count != number_of_weeks:
        print "Getting data from: " + chart.date
        for track in chart:
            # Add only unique songs since many track stay on the chart for
            # weeks
            if track.spotifyID not in id_list and track.spotifyID:
                id_list.append(track.spotifyID)
                song = {}
                song['artist'] = track.artist
                song['title'] = track.title
                song['track_id'] = str(track.spotifyID)
                try:
                    set_track_data(song, sp)
                    set_album_data(song, sp)
                    set_artist_data(song, sp)
                    set_audio_features(song, sp)
                except:
                    # if a spotify error occurs, refresh the token
                    sp = create_auth()
                    # write our data to a file just in case
                    write_list_of_dictionaries_to_file(
                        data, "BillboardBackupAt" + str(count) + ".csv")
                    continue

                data.append(song)
        chart = billboard.ChartData(name='hot-100', date=chart.previousDate)
        count += 1

    # Notify me when done
    Tkinter.Tk().bell()

    return data
