import pandas as pd

books_df = pd.read_csv('books.csv', on_bad_lines='warn')
books_groupby = books_df.groupby('authors')['bookID'].count().sort_values(ascending=False).reset_index()
print(books_groupby)

