# %%
import pandas as pd
import numpy as np
from IPython.core.display import display, HTML

display(HTML("<style>.container {width: 90% !important; }</style>"))

#read the data
data = pd.read_csv('books.csv', on_bad_lines='skip')
data.columns = data.columns.str.upper()

data
# %%
import dtale
dtale.show(data).open_browser()