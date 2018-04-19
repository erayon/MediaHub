from django.shortcuts import render
import pandas as pd
import numpy as np
import os
# Create your views here.
def home(request):
	pp = os.getcwd()
	loc = "/".join(pp.split("/")[0:-2])+"/MediaHub/Database/movies_details"
	print(pp)
	df = pd.read_pickle(loc+".pckl")
	name   = np.array(df['Movie_name'])
	MId    = np.array(df['ID'])
	rating = np.array(df['Rating'])
	pic    = np.array(df['CoverPic'])
	gen    = np.array(df['Generic'])
	year   = np.array(df['Year'])
	path   = np.array(df['path'])
	rng    = len(df)
	itemsz = []
	for i in range(len(df)):
	    #print(i)
	    # dict == {}
	    # you just don't have to quote the keys
	    an_item = dict(Mname=name[i],Mid=MId[i],Mrating=rating[i],Mpic=pic[i],Mgen=gen[i],Myear=year[i],Mpath=path[i])
	    itemsz.append(an_item)
	return render(request, 'myapp/index.html', {'items':itemsz})
