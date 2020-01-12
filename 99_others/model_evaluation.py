import pandas as pd
import numpy as np
import json

from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc, output_notebook
from bokeh.models import Select, HoverTool, ColumnDataSource, Legend
from bokeh.layouts import layout, gridplot

##################
# Create Source 1
##################
df = pd.read_csv('recalls.csv')
model_name = df.model_name.unique()[0]
source1 = ColumnDataSource(df.query('model_name == @model_name'))

##################
# Create Source 2
##################
def get_hist_data(probs, model_name):
    data, edges = np.histogram(probs, bins=100, range=(0, 1))
    return pd.DataFrame({
        'data': data, 
        'left': edges[:-1], 
        'right': edges[1:],
        'model_name': model_name
    })

with open('model_evaluation_data.json', 'r')as f:
    json_data = json.load(f)
    
df_hist = pd.concat([get_hist_data(probs, model_name) for 
                     model_name, probs in json_data['y_preds'].items()])
source2 = ColumnDataSource(df_hist.query('model_name == @model_name'))

def create_recall_comparison_figure():
    f = figure()

    f.toolbar_location=None
    f.toolbar.logo = None
    hover=HoverTool(tooltips=[
        ('Threshold','@threshold{0.00}'),
        ('Recall for Bad','@recall_bad{0.00}'),
        ('Recall of Good','@recall_good{0.00}')
    ])
    f.add_tools(hover)

    f.plot_width=650
    f.plot_height=400

    f.title.text = 'Model Evaluation'
    f.title.text_font = 'times'
    f.title.text_font_size = '25px'
    f.title.align = 'center'

    f.xaxis.axis_label = 'Threshold'
    f.yaxis.axis_label = 'Recall Scores'

    line_rb = f.line(x='threshold', 
                     y='recall_bad',
                     source=source1,
                     color='red')
    line_rg = f.line(x='threshold', 
                     y='recall_good',
                     source=source1,
                     color='green')
    legend = Legend(items=[
        ("Recall Of Bad", [line_rb]),
        ("Recall Of Good", [line_rg])
    ], location=(0, 220))
    f.add_layout(legend, 'right')

    return f

def create_prediction_histogram_figure():
    f = figure()

    f.toolbar_location=None
    f.toolbar.logo = None

    f.plot_width=650
    f.plot_height=400

    f.title.text = 'Prediction Probability Histogram'
    f.title.text_font = 'times'
    f.title.text_font_size = '25px'
    f.title.align = 'center'

    f.xaxis.axis_label = 'Prediction Probability (Bad to Good)'
    f.yaxis.axis_label = 'Count'

    f.quad(bottom=0, 
           top='data', 
           left='left', 
           right='right', 
           fill_color='blue', 
           source=source2)

    return f

def create_select_widget():
    
    def update_model_name(attr, old, new):
        model_name = select_widget.value
        source1.data = df.query('model_name == @model_name')
        source2.data = df_hist.query('model_name == @model_name')
        
    model_options=[(m, m) for m in df.model_name.unique()]
    select_widget = Select(title="Select Model", options=model_options)
    select_widget.on_change("value", update_model_name)
    return select_widget
    
f1 = create_recall_comparison_figure()
f2 = create_prediction_histogram_figure()
select_widget = create_select_widget()

curdoc().add_root(layout([[select_widget]]))
curdoc().add_root(gridplot([[f1, f2]], 
                           toolbar_location=None, 
                           toolbar_options={'logo': None}))