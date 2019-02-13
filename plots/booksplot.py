import pandas as pd

from bokeh.io import show, curdoc
from bokeh.layouts import layout
from bokeh.models import ColumnDataSource, FactorRange, HoverTool,CategoricalColorMapper
from bokeh.plotting import figure
from bokeh.themes import Theme
from bokeh.palettes import Category20_12

def color_picker(x):
    if len(x) == 0:
        return 'No awards'
    else:
        return 'One or more awards'


df=pd.read_pickle('data_figure1.pkl')
df['size']=df['num_reviews']/50
df['color']=df['awards'].map(lambda x: color_picker(x))
df['authors']=df['authors'].map(lambda x: " ".join(x))
df['num_awards']=df['awards'].map(len)

source = ColumnDataSource(df[['rating', 'num_ratings','size','color','title','authors','num_awards','num_reviews']])

hover = HoverTool(tooltips=[
    ("Title", "@title"),
    ("Author", "@authors"),
    ("Number of Awards", "@num_awards"),
    ("Number of Reviews", '@num_reviews')

])

color_mapper = CategoricalColorMapper(factors=['No awards', 'One or more awards'], palette=['#F44168', '#4286F4'], nan_color=Category20_12[0])
print(color_mapper)

p = figure(plot_height=600, plot_width=800, title="Romance Novel Ratings (size by number of reviews)", x_range=(0,20000),tools=[hover])
p.circle(x='num_ratings', y='rating',size='size',color={'field': 'color', 'transform': color_mapper}, line_color=None, fill_alpha=0.6,source=source,
legend='color')
p.legend.location='top_left'
p.xaxis.axis_label='Number of Ratings'
p.yaxis.axis_label='Average rating'

l = layout([
    [p]], sizing_mode='stretch_both')
#show(l)
curdoc().add_root(l)
