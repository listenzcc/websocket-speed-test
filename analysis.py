# %%
import json
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path


# %%


def load_log(log):
    lines = open(log).readlines()

    lst = ['{' + e.split('{')[1].split('}')[0] + '}' for e in lines]

    content = '[' + ','.join(lst) + ']'
    content = content.replace("'", '"')

    df = pd.DataFrame(json.loads(content))
    df = df.sort_values(by='idx')
    df.index = range(len(df))

    min_time = df['time'].min()
    df['procTime'] = df['time'].map(lambda t: t - min_time)

    return df


# %%
files = dict(
    multiProcessSlowResponse=Path('websocket-multi.log'),
    multiProcessFastResponse=Path('websocket-multi-2.log'),
    singleProcessSlowResponse=Path('websocket-single.log'),
    singleProcessFastResponse=Path('websocket-single-2.log'),
)

# %%
sns.set_theme()  # style="whitegrid")

fig1, axes1 = plt.subplots(2, 2, figsize=(12, 8))
axes1 = axes1.ravel()

fig2, axes2 = plt.subplots(2, 2, figsize=(12, 8))
axes2 = axes2.ravel()

j = -1

for title, log in files.items():
    j += 1

    df = load_log(log)

    kwargs = dict(
        title=title
    )

    if title == 'singleProcessFastResponse':
        df = df[df['total'] < 0.05]

    # px.scatter(df, x='procTime', y='total', color='recv', **kwargs).show()
    # px.scatter(df, x='total', y='recv', color='send', **kwargs).show()

    ax = axes1[j]
    sns.scatterplot(data=df, x='procTime', y='total', hue='send', ax=ax)
    ax.set_title(title)

    ax = axes2[j]
    sns.scatterplot(data=df, x='total', y='recv', hue='send', ax=ax)
    ax.set_title(title)

fig1.suptitle('Process time')
fig1.tight_layout()

fig2.suptitle('Response Time')
fig2.tight_layout()

plt.show()

fig1.savefig('Process-time.png')
fig2.savefig('Response-time.png')


# %%
