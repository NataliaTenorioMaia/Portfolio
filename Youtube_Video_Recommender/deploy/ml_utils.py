# All functions needed to compute predictions

import pandas as pd
import joblib as jb
from scipy.sparse import hstack, csr_matrix
import numpy as np
import json

# Trained models:
clf_rf = jb.load("random_forest_2021.pkl.z")
clf_lgbm = jb.load("lgbm_2021.pkl.z")
# Trained vectorizer:
title_vec = jb.load("title_vectorizer_2021.pkl.z")

# FUNCTIONS WHICH TRANSFORM THE FEATURES =========================================================================
def categ(x):
    if (x==['Autos & Vehicles'] or x==['Gaming'] or x==['Comedy'] or
        x==['Sports'] or x==['Pets & Animals'] or x==['Music']): return 0
    elif (x==['Film & Animation'] or x==['Howto & Style']): return 1
    elif (x==['People & Blogs'] or x==['Entertainment']): return 2
    elif x==['Education']: return 3
    elif x==['Science & Technology']: return 4
    elif x==['News & Politics']: return 5
    elif x==['Nonprofits & Activism']: return 6
    else: return 0

def durat(x):
    t = x/60
    if t<=30: return 0
    elif t>30 and t<=70: return 1
    else: return 2

def view(data):
    if 'view_count' in data.keys():
        x = data['view_count']
        if x<=50: return 0
        elif x>50 and x<=1e3: return 1
        elif x>1e3 and x<=1e5: return 2
        else: return 3
    else: return 0

def like_ra(data):
    if (('like_count' in data.keys()) & ('dislike_count' in data.keys())):
        if data['like_count']==0: return 1
        else:
            ratio = data['dislike_count']/data['like_count']
            if ratio>0.1: return 0
            else: return 1
    else: return 0
    
def ch_appeal(channel_name):
    list_3 = ['study','mit ','lex ','amini','proj','brunton']
    list_2 = ['tedx','stanford','marr','youtube','online']
    list_1 = ['school','sci','lab','google','krish','course']

    l3 = [True for word in list_3 if word in channel_name]
    l2 = [True for word in list_2 if word in channel_name]
    l1 = [True for word in list_1 if word in channel_name]
    if any(l3): return 3
    elif any(l2): return 2
    elif any(l1): return 1
    else: return 0
    
# FUNCTION WHICH RETURNS THE CLEAN DATASET ===========================================================
def compute_features(data):
    """Creates the same features which we used to train the models. """
    
    categories     = categ(data['categories'])
    duration       = durat(data['duration'])
    views          = view(data)
    channel_appeal = ch_appeal(data['uploader'].lower())
    like_ratio     = like_ra(data)
    title          = data['title']

    features = dict()

    features['categ']          = categories
    features['duration']       = duration
    features['views']          = views
    features['like_ratio']     = like_ratio
    features['channel_appeal'] = channel_appeal
    features['title']          = title

    vectorized_title = title_vec.transform([title])

    feats=csr_matrix(np.array([features['categ'],features['duration'],features['views'],features['like_ratio'],features['channel_appeal']]))
    feature_array = hstack([feats, vectorized_title])
    return feature_array

# FUNCTION WHICH RETURNS THE PREDICTION ===========================================================
def compute_prediction(data):
    """Computes the scores of the new videos. """
    
    feature_array = compute_features(data)
    #print(feature_array)
    if feature_array is None:
        return 0

    p_rf = clf_rf.predict_proba(feature_array)[0][1]
    p_lgbm = clf_lgbm.predict_proba(feature_array)[0][1]
    p = 0.1*p_rf + 0.9*p_lgbm
    #log_data(data, feature_array, p)
    return p

def log_data(data, feature_array, p):
    """ This is for debugging purposes. """
    #print(data)
    video_id = data.get('og:video:url', '')
    data['prediction'] = p
    data['feature_array'] = feature_array.todense().tolist()
    print(video_id, json.dumps(data))







