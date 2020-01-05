from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Range1d
from bokeh.plotting import figure
from datetime import datetime
from math import sin, cos

increment = 0.15

#create figure
f=figure()

#create ColumnDataSource
source_sine=ColumnDataSource(dict(x=[0],y=[sin(0)]))
source_cosine=ColumnDataSource(dict(x=[0],y=[cos(0)]))

#create glyphs
f.line(x='x',y='y',source=source_sine, legend='sine', color='red')
f.line(x='x',y='y',source=source_cosine, legend='cosine', color='blue')
f.y_range=Range1d(start=-1.5, end=1.5)

#create periodic function
def update():
    last_x = source_sine.data['x'][-1]
    new_data=dict(x=[last_x + increment],y=[sin(last_x + increment)])
    source_sine.stream(new_data,rollover=100)

    last_x = source_cosine.data['x'][-1]
    new_data=dict(x=[last_x + increment],y=[cos(last_x + increment)])
    source_cosine.stream(new_data,rollover=100)

#add figure to curdoc and configure callback
curdoc().add_root(f)
curdoc().add_periodic_callback(update,100)
