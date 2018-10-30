import plotly.graph_objs as go
import pandas as pd
import plotly


# colorscale
colors = [
    'rgba(68, 1, 84, 1)', 'rgba(72, 21, 103, 1)', 'rgba(72, 38, 119, 1)',
    'rgba(69, 55, 129, 1)', 'rgba(64, 71, 136, 1)', 'rgba(57, 86, 140, 1)', 'rgba(51, 99, 141, 1)', 'rgba(45, 112, 142, 1)', 'rgba(40, 125, 142, 1)', 'rgba(35, 138, 141, 1)', 'rgba(31, 150, 139, 1)', 'rgba(32, 163, 135, 1)', 'rgba(41, 175, 127, 1)', 'rgba(60, 187, 117, 1)', 'rgba(85, 198, 103, 1)', 'rgba(115, 208, 85, 1)', 'rgba(149, 216, 64, 1)', 'rgba(184, 222, 41, 1)', 'rgba(220, 227, 25, 1)', 'rgba(253, 231, 37, 1)']


def main():
    # carrega as bases
    champion_df = pd.read_csv('data/champs.csv')
    matches_df = pd.read_csv('data/matches.csv', usecols=['id', 'seasonid'])
    teambans_df = pd.read_csv('data/teambans.csv', usecols=['matchid', 'championid'])

    # renomeia algumas colunas de interesse para o natural join
    champion_df.rename(columns={'name': 'champion', 'id': 'championid'}, inplace=True)
    matches_df.rename(columns={'id': 'matchid'}, inplace=True)

    # faz o join das colunas
    df = teambans_df.join(matches_df.set_index('matchid'), on='matchid').join(champion_df.set_index('championid'), on='championid')

    graph1(df)
    graph2(df)


# GRÁFICO 1: campeões mais banidos por temporada
def graph1(df):
    # agrupa dado por temporadas
    seasons = df.groupby('seasonid')

    # guarda por temporada, o campeão e porcentagem de bans
    ban_rate = []

    for s in seasons:
        # pega o total de bans da season
        s_total = s[1].shape[0]

        s_champs = pd.DataFrame(s[1])
        s_champs = s_champs.groupby('champion')

        # separa campeões e sua porcentagem de ban
        champions = []
        for c in s_champs:
            champions.append((c[0], (c[1].shape[0]/s_total)*100))

        # classifica melhores
        champions.sort(key=lambda x: x[1], reverse=True)
        champions, bans = map(list, zip(*champions))

        ban_rate.append({'y': champions, 'x': bans})

    data = []

    data.append(go.Bar(
            x=ban_rate[0]['x'][:20],
            y=ban_rate[0]['y'][:20],
            orientation='h',
            marker = dict(
                color=colors,
                line=dict(
                    color='rgba(58, 71, 80, 0.6)',
                    width=2)
    )))

    for i in range(1, len(ban_rate)):
        data.append(go.Bar(
            x=ban_rate[i]['x'][:20],
            y=ban_rate[i]['y'][:20],
            orientation='h',
            visible=False,
            marker = dict(
                color=colors,
                line=dict(
                    color='rgba(58, 71, 80, 0.6)',
                    width=2)
            )))

    updatemenus = list([
        dict(active=0, buttons=list([
                dict(label='Season 3', method='update', args=[{'visible': [True, False, False, False, False, False]}]),
                dict(label='Season 4', method='update', args=[{'visible': [False, True, False, False, False]}]),
                dict(label='Season 5', method='update', args=[{'visible': [False, False, True, False, False, False]}]),
                dict(label='Season 6', method='update', args=[{'visible': [False, False, False, True, False, False]}]),
                dict(label='Season 7', method='update', args=[{'visible': [False, False, False, False, True, False]}]),
                dict(label='Season 8', method='update', args=[{'visible': [False, False, False, False, False, True]}]),
            ]),
            direction='right', pad={'r': 10, 't': 10}, showactive=True, xanchor='left', yanchor='top', x=0.1, y=1.1
        )
    ])

    annotations = [dict(text='', x=0, y=10, showarrow=False)]

    layout = dict(
        title='Campeões Mais Banidos em Partidas Ranqueadas',
        showlegend=False,
        updatemenus=updatemenus,
        annotations=annotations,
        xaxis={'title': 'Porcentagem de Banimentos'})

    fig = dict(data=data, layout=layout)
    plotly.offline.plot(fig, auto_open=True)


def graph2(df):
    pass


if __name__ == '__main__':
    main()
