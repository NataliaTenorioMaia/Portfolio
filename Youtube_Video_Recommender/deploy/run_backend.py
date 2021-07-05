# Code used to update the database in db_starter.py

from ml_utils import compute_prediction # Pre-defined functions
import sqlite3 as sql                   # Structured Query Language
import youtube_dl                       # Youtube scraper
import json 

# We have to use the same queries that we used to train our model if we want the results to make sense:
queries = ["artificial+intelligence", "machine+learning", "deep+learning"]
db_name = 'videos.db' # database name

def update_db():
    """ Updates our video database with predictions. """
    
    ydl = youtube_dl.YoutubeDL({"ignoreerrors": True})

    # connect() opens a connection to the SQLite database file:
    with sql.connect(db_name) as conn: 
        # Extracting the new videos data for each query at a time:
        for query in queries:
            # We collect data for the 40 most recent videos:
            r = ydl.extract_info("ytsearchdate80:{}".format(query), download=False)
            video_list = r['entries']

            # For each video, computes the "appeal" score and stores the desired features in the database videos.db:
            for video in video_list:
                if video is None:   # this prevents the loop from breaking in case of errors
                    continue

                p = compute_prediction(video)  # here we use a function from ml_utils which returns the appeal score

                video_id = video['webpage_url']
                watch_title = video['title'].replace("'", "") 
                # data_front is the dictionary that we will insert into the database videos.db:
                data_front = {"title": watch_title, "score": float(p), "video_id": video_id} 
                print(video_id, json.dumps(data_front))
                # The basic purpose of a "cursor" is to point to a single row of the result
                # fetched by the query. We load the row pointed by the cursor object.
                c = conn.cursor()
                # the "**" tells format() to access the keys of the dictionary data_front:
                c.execute("INSERT INTO videos VALUES ('{title}', '{video_id}', {score})".format(**data_front)) #, {update_time}
                # Now we save the changes in the db_name database:
                conn.commit()
    return True
