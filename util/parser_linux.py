from pathlib import Path
import os
from tqdm import tqdm
import numpy as np
import re
import string
from nltk.tokenize import word_tokenize
import PTN
from imdb import IMDb
import pandas as pd
from sys import platform


def get_movies_list():
    temp = []
    for root, dirs, files in os.walk("/"):
        for file in files:
            if file.endswith(".mkv") or file.endswith(".mp4") or file.endswith(".mpeg") or file.endswith(".mpg"):
                temp.append(os.path.join(root, file))
    return temp

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def considerMovies(videos):
    temp = []
    not_allowd = ['KB']
    pathofmovies = []
    for idx,i in enumerate(videos):
        if file_size(i).split(" ")[-1] not in not_allowd:
            if file_size(i).split(" ")[-1] == 'MB':
                if float(file_size(i).split(" ")[0]) >= 600:
                    temp.append([file_size(i).split(" "),videos[idx]])
                    pathofmovies.append(i)
            if file_size(i).split(" ")[-1] == 'GB':
                temp.append([file_size(i).split(" "),videos[idx]])
                pathofmovies.append(i)
    movies = [i[1] for i in temp ]
    size = [i[0] for i in temp]
    movies_ = []
    for idx,mov in enumerate(movies):
        val  = mov.split("/")[-1]
        val2 = " ".join(val.split(".")[0:-1])
        #print(val2)
        info = PTN.parse(val2)
        movies_.append([size[idx],info['title'],pathofmovies[idx]])
    return movies_

def getPathforDatabase():
    loc  = os.getcwd()
    location = "/".join(loc.split("/")[0:-1])+"/Database/movies_details"
    return location


def create_table(videos,csd):
    id_ = []
    ia = IMDb()
    for movies_name in tqdm(csd):
        try:
            s = ia.search_movie(movies_name[1])
            dp = s[0]
            ia.update(dp)
            id_.append([movies_name[1] + " Movie Id: "+dp.movieID, movies_name[-1]])
        except Exception as e:
            print(e)
    IDnM = [i[0] for i in id_]
    pthMov = [i[1] for i in id_]
    id_key = [k.split(":")[-1] for  k in IDnM]
    names = [i.split("Movie Id")[0] for i in IDnM]

    Database = []
    for idx,each_movies in enumerate(tqdm(id_key)):
        try:
            ID = each_movies.split(":")[-1]
            MOVIE = names[idx]
            dpx = ia.get_movie(ID)
            Database.append([MOVIE,ID,dpx['rating'],dpx['full-size cover url'],dpx['genres'],dpx['year'],pthMov[idx]])
        except Exception as e:
            print(e)

    col = np.array(['Movie_name','ID','Rating','CoverPic','Generic','Year','path'])

    df  = pd.DataFrame(Database,columns=col)
    df.to_csv(getPathforDatabase()+".csv")
    df.to_pickle(getPathforDatabase()+".pckl")
