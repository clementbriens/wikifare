import requests
import json
import wikipedia
import pandas as pd
import time
import matplotlib


df = pd.DataFrame(columns=['revid', 'parentid','user', 'timestamp'])


def get_data(query, use_time):
    base_url = "http://en.wikipedia.org/w/api.php"
    if use_time is None:
        parameters = { 'action': 'query',
                   'format': 'json',
                   'continue': '',
                   'titles': query,
                   'prop': 'revisions',
                   'rvprop': 'user|timestamp|ids',
                   'rvlimit': 'max'}

    else:
        parameters = { 'action': 'query',
                   'format': 'json',
                   'continue': '',
                   'titles': query,
                   'prop': 'revisions',
                   'rvprop': 'user|timestamp|ids',
                   'rvlimit': 'max',
                   'rvendid' : use_time}

    wp_call = requests.get(base_url, params=parameters)
    print(wp_call)
    response = wp_call.json()
    return response




def scrape_section(query, use_time, df):
    response = get_data(query, use_time)
    for page in response['query']['pages']:
        for revision in response['query']['pages'][page]['revisions']:
            df.loc[len(df)] = revision
    return df


query = 'Taiwan'
scope = 1

for x in range (0,2):
    print('scraping {} section {}'.format(x, query))
    if x == 0:
        use_time = None
    else:
        use_time = df['revid'][-1:]
        print(use_time)
    df = scrape_section(query, use_time, df)


print(df)
df.to_csv('wikifare_{}.csv'.format(query))

# df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
# df.index = df['timestamp']
# del df['timestamp']
#
# df.plot(y = df.resample('D').sum(),
# title = '"{}" Wikipedia daily edits'.format(query)
# ).get_figure().savefig('wikifare_{}_2.png'.format(query))
#
# time_series.plot().get_figure().savefig('wikifare_{}_2.png'.format(query))
