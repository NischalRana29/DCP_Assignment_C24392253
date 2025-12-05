import pandas as pd

#importing dataset 
df1 = pd.read_csv('data/album.csv')
df2 = pd.read_csv('data/albumtracktune.csv')

print("********************************************")
print("First dataset:")
print(df1.head())
print(df1.tail())
print(df1.shape)
print(df1.info())
print(df1.describe())
print("********************************************")


#task 1.1, count of album in dataset, column names, artist appear in first and last 5 albums 
print("\n********************************************")
print("Number of albums:", df1.shape[0])
print("Column names:", df1.columns.tolist())
print("Artists in first 5 albums:", df1.head()['artist'].tolist())
print("Artists in last 5 albums:", df1.tail()['artist'].tolist())
print("********************************************")


#code to find missing values
print("\n********************************************") 
print(df1.info())
print("Missing values:\n", df1.isnull().sum())
print("********************************************")




print("\n********************************************")
print("Second dataset: ")
print(df2.head())
print(df2.tail())
print(df2.shape)
print(df2.info())
print(df2.describe())
print("********************************************")



#code for unique artists 
print("********************************************")
unique_artists = df1['artist'].unique()
print("Number of unique artists:", len(unique_artists))
print("Artists:", unique_artists)
print("********************************************")


# Number of tracks
print("Number of tracks:", df2.shape[0])

# Column names
print("Columns:", df2.columns.tolist())

# Relationship
print("Album ID refers to the album each track belongs to.")

# Highest track number
print("Highest track number:", df2['track_num'].max())

# Max tunes per track
print("Max tunes in a track:", df2['tune_num'].max())

# Most frequent tune titles
print("Most common tune titles:\n", df2['tune_num'].value_counts().head(10))

#part 3.1
for artist in ["Altan", "Martin Hayes", "The Bothy Band"]:
    filtered = df1[df1['artist'] == artist]
    print(f"{artist} has {filtered.shape[0]} albums")
    print(filtered[['id', 'title']])

#part 3.2
album1_tracks = df2[df2['album_id'] == 1]
print("Tracks on album_id 1:", album1_tracks['track_num'].nunique())
print("Total tunes on album_id 1:", album1_tracks['tune_num'].sum())

#part 3.3
multi_tune_tracks = df2[df2['tune_num'] > 1]
print("Tracks with multiple tunes:", multi_tune_tracks.shape[0])

"""
#part 4.1
tracks_per_album = df2.groupby('album_id')['track_num'].nunique()
print("Album with most tracks:\n", tracks_per_album.sort_values(ascending=False).head(1))
"""

#part 4.2
tunes_per_album = df2.groupby('album_id')['tune_num'].sum()
print("Tunes per album:\n", tunes_per_album)