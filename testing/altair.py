# import altair with an abbreviated alias
import altair as alt
import numpy as np
import pandas as pd
from data_structures.compressed_vector import CompressedVector as cv
import sdsl4py
import sys
# load a sample dataset as a pandas DataFrame
from vega_datasets import data
cars = data.cars()
og_x = cars['Horsepower'].values
og_y = cars['Miles_per_Gallon'].values
# Extract data as numpy arrays
x = cv(
    int_width=16,
    decimal_places=2,
    get_decompressed=False
)
x.create_vector(len(og_x))
x.fill_from_vector(og_x)
x.compress(sdsl4py.dac_vector)

y = cv(
    int_width=16,
    decimal_places=2
)
y.create_vector(len(og_y))
y.fill_from_vector(og_y)
y.compress(sdsl4py.dac_vector)
# Create a new DataFrame with our numpy arrays
data = pd.DataFrame({
    'Horsepower': x,
    'Miles_per_Gallon': y,
    'Origin': cars['Origin']  # Keep the origin for color encoding
})

# make the chart
chart = alt.Chart(data).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
).interactive()

# Save to HTML file
chart.save('cars_chart.html')
print("Chart saved to cars_chart.html - open this file in your browser")
print(f"Size of compressed_vector x: {x.size_in_bytes()} bytes, y: {y.size_in_bytes()} bytes.")
print(f"Size of original_vector x: {og_x.nbytes} bytes, y: {og_y.nbytes} bytes.")