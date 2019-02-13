import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter
from bokeh.io import curdoc
from bokeh.layouts import widgetbox, layout
from bokeh.models.widgets import CheckboxGroup
from bokeh.palettes import Set2

Spectral6=Set2[6]

# Set up data

plot_data=pd.read_pickle("themes_time_bigger.pkl")


plot_data=plot_data[plot_data['dts']>=pd.to_datetime('01-01-2013')]
x = plot_data['dts']

source = ColumnDataSource(data=dict(x=x,
                                    y1=plot_data['Royalty'],
                                    y2=plot_data['Military'],
                                    y3=plot_data['Supernatural'],
                                    y4=plot_data['Holiday'],
                                    y5=plot_data['Bdsm'],
                                    y6=plot_data['Adventure']))

# Set up plot
plot = figure(plot_height=400, plot_width=800, title="Themes",tools="crosshair,pan,reset,save,wheel_zoom")

plot.line(x='x', y='y1', source=source, line_width=3, line_alpha=0.6,legend='Royalty',color=Spectral6[0])
plot.line(x='x', y='y2', source=source, line_width=3, line_alpha=0.6,legend='Military',color=Spectral6[1])
plot.line(x='x', y='y3', source=source, line_width=3, line_alpha=0.6,legend='Supernatural',color=Spectral6[2])
plot.line(x='x', y='y4', source=source, line_width=3, line_alpha=0.6,legend='Holiday',color=Spectral6[3])
plot.line(x='x', y='y5', source=source, line_width=3, line_alpha=0.6,legend='BDSM',color=Spectral6[4])
plot.line(x='x', y='y6', source=source, line_width=3, line_alpha=0.6,legend='Adventure',color=Spectral6[5])

plot.xaxis.formatter=DatetimeTickFormatter(
        hours=["%B %Y"],
        days=["%B %Y"],
        months=["%B %Y"],
        years=["%B %Y"],
    )
plot.xaxis.major_label_orientation = np.pi/4


plot.legend.location = "top_center"
plot.legend.orientation = "horizontal"

plot.legend.click_policy="hide"
l=layout(responsive=True,children=[plot])
curdoc().add_root(l)
