from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.plotting import figure
from random import randrange
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from math import radians

#create figure
f=figure()

#create webscraping function
def extract_value():
    r=requests.get("http://bitcoincharts.com/markets/bitflyerJPY.html",headers={'User-Agent':'Mozilla/5.0'})
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    value_raw=soup.find_all("p")
    value_net=float(value_raw[0].span.text)
    return value_net

#create ColumnDataSource
source=ColumnDataSource(dict(x=[datetime.now()],y=[extract_value()]))

#create glyphs
f.circle(x='x',y='y',color='olive',line_color='brown',source=source)
f.line(x='x',y='y',source=source)
f.xaxis.major_label_orientation=radians(90)
f.xaxis.formatter=DatetimeTickFormatter(
    seconds=["%Y-%m-%d-%H-%m-%S"],
    minsec=["%Y-%m-%d-%H-%m-%S"],
    minutes=["%Y-%m-%d-%H-%m-%S"],
    hourmin=["%Y-%m-%d-%H-%m-%S"],
    hours=["%Y-%m-%d-%H-%m-%S"],
    days=["%Y-%m-%d-%H-%m-%S"],
    months=["%Y-%m-%d-%H-%m-%S"],
    years=["%Y-%m-%d-%H-%m-%S"],
    )
    
#create periodic function
def update():
    new_data=dict(x=[datetime.now()],y=[extract_value()])
    source.stream(new_data,rollover=200)

#add figure to curdoc and configure callback
curdoc().add_root(f)
curdoc().add_periodic_callback(update,2000)
