# Now That's What I Call Music Classifier

## Table of Contents
1. [Description](#description)
2. [Backstory](###backstory)
3. [Update - Feb 5th, 2018](##Update)
4. [Project Overview](##Project-Overview)
5. [How to use](##How-to-use) 
6. [Contents](##Contents)

### Description

I was mostly interested in this project because I wanted to put my data wrangling and machine learning skills to the test with a fun subject matter.

I did not expect any level of success; only to end up having some fun, improving my coding skills, and maybe learning something new.

I was suprised to see that I had **84% accuracy** in classfying whether or not a song had appeared on a Now album in my test data.

### Backstory

A few weeks ago (Jan 2017) I heard that a new Now That's What I Call Music (NWCM) album was going to be released; the collection's 61st volume. As someone who fondly remembers these CDs, I thought it would be fun to try and automate the song selection process by picking tracks off the most recent Billboard Top 100 Charts that best resembled songs selected on previous albums.

So I put my knowledge of Python, web scraping, and sklearn to the test and built a model capable of making some predictions from today's popular music.

If you are interested in following along with my journey, read the following sections in the README and open up the NWCM Walkthrough notebook.

## Update

#### February 5th, 2018

It has been almost a full years since I made my initial predictions and I managed to guess....0 songs correctly.
That's right, not a single song I predicted made it onto the 62nd volume of NWCM.

Not only did I not get a single prediction right for vol. 62, but volumes 63, 64, and 65 are now available, and as you might guess, I didn't manage to guess a single song on either of those albums (I did however guess artists who were later featured, so that's a start).

That's ok though when you have 0% accuracy, the only place to go is up!

Here is what I have learned since.

### Now Album Creation

Shortly after finishing my model, I found an article about how the creator ("Moskow") creates his hit compilation albums.
As it turns out, the early albums were mostly based off Billboard Top 100 Charts (this is the domain my training data was selected from), but now with the streaming era, "Moskow" mentioned he looks at popularity figures from the popular streaming services.

After assembling a list of songs that remained popular over an extended period, "Moskow" would attempt to obtain their licenses.
Once he has enough tracks to fill a CD he works on making a cohesive, "sequenced" album.
Note, the sequencing happens after songs have been cleared.

### How would I approach this differently in a second round?

Now that I know a bit more about the process and have learned that audio features really play no part in a songs selection, I would shift emphasis of my predictive features from audio features to:

- popularity
- likelihood of "clearing" a song (i.e. obtaining its license)
- "sequence"-ability (making sure the album "flows")

For popularity, I would definitely continue to use the artist and song popularity scores from Spotify.
I would also be interested in reopening the search for a new source of artist/song popularity in order to form a composite popularity score; so that Spotify is not the single source of truth for popularity.
This has been an area of concern for my predictive modeling at work, and despite testing out a normalized play count from Nielsen, my vote still resides with Spotify.
One thing I learned during this process was that Spotify popularity rankings decay over time if the play count for a song/artist is not above a certain threshold.
There is no way (to my knowledge) to pull historical popularity, so perhaps I'd be interested in recording these daily myself and using "rate-of-decay" as a feature.

For likelihood of clearing; adding a value for how many songs a label has cleared for NWCM in the past OR whether this record label has ever cleared songs before are the low hanging features.
My gut tells me that if Moskow has cleared songs from Record Co XYZ in the past, he is more likely to clear with them again (as opposed to an unkown label); I don't feel this is much of a reach.
Also lets be honest, cost is a huge factor. I don't think clearing fees are publicly available but if I can think of something to estimate or categorize a clearing fee, I will use it.

Finally "sequence"-ability. This is really where this project opens itself up to analysis again.
I'd have to get a bit more involved with genre-classification here to determine how Moskow balances an album between pop, edm, and hip-hop.

In terms of how the predictions are made, I would definitely change the format.
Since there has to be "sequence"-ability to the album, I can't just choose 25 edm songs if they have high similarity ratings to previous Now selections.

Rather than releasing 1 album guess, I'd provide a 100-150 song ranked list to better mimic Moskow's process of calling labels with songs on the Billboard Top 100.

### Code Quality

Modeling changes aside, I have spent the last year scraping, cleaning, transforming all sorts of data.
This has increased the amount of code I get to write tremendously, and pressured me to write cleaner, less coupled, more extensible code.
Looking back at this project has been rewarding in that I can see how far my coding abilities have come.

If I choose to pursue a second iteration of this model, I would definitely leverage what I have learned working with pandas daily.

Top issues I've noticed:

- Reliance on accuracy for model evaluation. I really, really should have incorporated precision and recall in my model selection process and created a confusion matrix to figure out my counts for false positives and true negatives.
- Dealing with data hygiene is a bit clunky. It looks like I applied hygiene as each row was pulled from a scraper or API. In a second attempt I would pull all my data, appending each source to its own dataframe, then use the .pipe method in pandas to push the frame through a pipe of hygiene functions.
- Lack of dataframe use. Transformations & data IO is so much cleaner when you use processing frameworks like pandas. In this project I really tried to stick to using dictionaries and lists but I could have saved myself a ton of trouble by appending scraping results to a dataframe, passing that frame through a pipeline of cleaning functions, and then joining separate frames containing other features in the step before training my model.
- Hard coding everywhere. I see that in my `set_spotify_data()` function, I return `None` if the song passed into the function is authored by Taylor Swift. This is terrible form, instead I should have used an optional argument to provide a list of values to exclude.

Realistically, I will not go back and work this project.

It was a fun idea, I love to talk about it, its quirky, and shows a little bit about who I am and how I think.
However my list of personal projects is stacked sky high and my free time is limited.

I would rather take the lessons learned here and apply them to my next project (recommendation system for free Yoga videos anyone?)

-- Drew

## Project Overview

### Initial Project planning questions

Do I have enough data?

- I scraped 1220 songs from 61 Now That's What I Call Music albums to form the Now-labeled items. For training data without the Now label, Billboard Top 100 data is available from this week to well before the Now albums were released.

Can you state a clearly defined question to be answered by this project?

- Can we simplify the next Now album creation by returning a list of songs evaluated by their similarity (in terms of audio features) to previous Now album song selections?

  The success of this process would be measured by how many of the songs we return in our list appear on the next album.

Are you confident in the available to data's ability to answer the project's question?

 - Not really but I'd still like to see how far I get. I think the process for selecting tracks for an album is not an exact science. The available data might be better for creating a classifier to determine if a newly released song will make it on the Billboard Top 100.

### Feature Selection

![feature corr](https://github.com/drewhontz/Now/blob/master/img/fc.JPG "Feature Correlation")

When selecting features it was important to look for **correlation** with the target (Now appearance or not), any **outliers** in the training set, and any gaping **missing values**.

The popularity features displayed a high amount of correlation with our target, so they were retained. The audio features that were used were selected based on F-scores resulting from a SelectKBest test where k=5.

How would we define an outlier here? A slow jam or country song that made it on a mostly pop/edm album?
There were not any tracks that had significantly lower popularity or audio features that I included in the training set so no outlier removal was performed.

Imputation was not necessary as our set was small enough that I could manually correct any missing data.

Data hygiene was necessary to correct artist and song names from billboard or wikipedia for use in querying their audio features in the Spotify API.

The ideas for these features were mostly "intuition"-based; I have no insight into how the selection process works so this is how I'd approach track selection if I wanted this to be an automated process.

Once the features were scraped, I used SelectKBest to select the 5, 7, and 11 features with the most significant F-scores.
5 features had the best accuracy with all the models so I went ahead with: `album_popularity`, `artist_popularity`, `energy`, `loudness`, and `track_popularity`.

I did not use any PCA to reduce our data's dimensionality. I wanted to create a composite "popularity score" that combined the artist and song popularity from multiple sources but I was surprised at the lack of available popularity data.

No text features were used, and no scaling was required.

### Model Selection

The type of model was selected based off the highest accuracy figures in test.
This problem was modeled as a supervised classification problem so I narrowed down my options to SVM, Decision Trees, and a KNN type classifier.

The KNN classifier had the highest accuracy, so that is what I used for our predictions.
When re-examining this project I regret not including and ROC curve plot showing precision, recall, or F1 scores.

## How to Use

To follow along with the creation of our classifier, all the content you need is in `NWCM Walkthrough.ipynb`. Here you can run each cell and see the process evolve from data collection to making predictions. **Pro-Tip**: Download the datasets mentioned below rather than running my scraping cells and it will save you about 30 minutes

## Contents

### Notebooks

- `NWCM Walkthrough.ipynb` : This is where the magic happens! This is the main notebook outlining the process of data wrangling, feature selection, algorithm evaluation, making our predictions, and a discussion on current problems and improvements to be made

- `Analysis - NWCM.ipynb` : There were some assumptions I thought I would investigate during the process of completing this project so I included an analysis with some nice visualizations from Tableau

### Visualizations

- To view some of the vizualizations I created during this project, please visit the following [Tableau Public link](https://public.tableau.com/profile/athontz#!/vizhome/NWCMVisualizations/NWCMVisualizations).

### Datasets

- `NWCM_Spotify_Features.csv` : Now tracklist and album data joined with each songs spotify audio features

- `Billboard_Spotify_Features.csv` : The last N weeks of unique Billboard Top 100 chart data and their Spotify audio features

- `corrections.csv` : A csv file I manually enter spotify id's into to update my `NWCM_Spotify_Features.csv` file where songs are in spotify but my search query had trouble finding

- `TrainingData.csv` : The joined result of `NWCM_Spotify_Features.csv` and `Billboard_Spotify_Features.csv` with a column for now labels

### Convenience Functions

- `/utils/billboard_utils.py` : Includes functions to scrape Billboard Top 100 Chart data (via Python module billboard)

- `/utils/spotify_utils.py` : Includes functions to query Spotify Web Api (via Python module spotipy) for Spotify features used in our data model

- `/utils/utils.py` : Contains mostly i/o related convenience functions such creating in and out files from list of Python dictionaries

- `/utils/wiki_scrape` : convenience functions for scraping links and track listings from wikipedia. Leverages urllib and BeautifulSoup4 from python
