import pandas as pd
import urls_n_filenames from urls_to_scrape
import json

# where tha magic happens
for u_n_f in urls_n_filenames:

df = pd.DataFrame()

num_movies = 0

# where tha magic happens
for u_n_f in urls_n_filenames:
    # load json file in
    print(f'Opening {u_n_1[0]}.json')

    with gzip.GzipFile(f'./json_data/{u_n_f[1]}', 'r') as json_file:
        print(f'Pushing {u_n_f[1]} to csv')
        json_data = json.loads(json_file.read().decode('utf-8'))

        # loop through json and append each movie into a dataframe
        for movie_hash in json_data:
            # `[[*json_data[movie_hash]]]` ensures correct column ordering
            df = df.append(json_data[movie_hash], ignore_index=True)[[*json_data[movie_hash]]]

            # for logging progress
            num_movies += 1
    

        print(f'Done pushing {file} to csv. {num_movies} movies appended to csv.')

print(df.shape)

# save output to a csv
df.to_csv('movie-budgets.csv')