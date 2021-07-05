# This is the main code of the recommender web application, it's where everything comes together.

from flask import Flask, request, render_template  # Web application framework
import json                                        # JavaScript Object Notation module to handle database
import run_backend                                 # Script for web scraping and computing predictions
import ml_utils                                    # Script with machine learning model
import sqlite3 as sql                              # Handles database
import youtube_dl                                  # Youtube scraper module
import os.path                                     # Allows us to use functionalities of our OS
import os           

#-----------------------------------------------------------------------------------

# First we create a Flask object so the server understands our commands:
app = Flask(__name__)

def removeDuplicates(lst):
    """Removes duplicates from list of tuples."""    
    return list(set([i for i in lst]))

def get_predictions():
    """Calls run_backend to load the predictions for the
    new videos, accompanied by their titles and urls.
    Then, organizes and formats results."""

    videos = []

    # Reads the SQL database and organizes the data in the list "videos":
    with sql.connect(run_backend.db_name) as conn:
        c = conn.cursor()
        for line in c.execute("SELECT * FROM videos"):
            line_video = {"title": line[0], "video_id": line[1], "score": line[2]} #, "update_time": line[3]
            videos.append(line_video)
			
    # Takes the list of dictionaries "videos" and writes it as simple tuples of values for each feature:
    predicts = []
    for video in videos:
        predicts.append( ( video['video_id'], video['title'], float(video['score']) ) )

    # Removes duplicates:
    predictions = removeDuplicates(predicts)

    # Sorts all results starting from the highest score:
    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:20]

    return predictions

# We use this decorator to indicate to Flask where it should direct the requests.
# This means that when we make a request to "/", which is simply the root directory of
# our application, this decorator returns the result of the main_page function.
@app.route('/')
def main_page():
    """Calls the function get_predictions and, using html code,
     returns its result formated as a table."""
    
    preds = get_predictions() # gets the predictions of the new videos

    return render_template('index.html', predictions = preds)

# To understand the conditional below, read the following article:
# https://medium.com/@ayushpriya10/why-do-we-use-if-name-main-in-python-cb77b95e0ce7#
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
