# Biblioteca de funções para analise de dados.

import pandas as pd
import numpy as np
import matplotlib as mat
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

colormap: str = None

def main() -> None:
    None

def set_palette(colormap: str) -> mat.colors.ListedColormap:
    return sns.color_palette(colormap)

### Tabelas

def frequencia_cat(dataframe: pd.DataFrame, coluna: str, plot: bool=False) -> pd.DataFrame:
    """
    Exibe as frequências e porcentagens das categorias de uma determinada coluna
    :param dataframe: dataframe 
    :param coluna: Coluna do dataframe que possue as categorias
    :return: Um dataframe com as informações     
    """
    data = dataframe[coluna].agg(['value_counts'
                                ,lambda x : (x.value_counts() / dataframe.shape[0])*100]).reset_index().rename(columns={'index':coluna
                                                                                                                        ,'value_counts':'frequencia'
                                                                                                                        , '<lambda>':'porcentagem'}).sort_values(by='porcentagem'
                                                                                                                                                                , ascending=True)
    if plot:
        return data
    else: 
        return data.style.background_gradient(cmap=colormap, high=.5, subset=["porcentagem"])     

def grpby_2cat(dataframe: pd.DataFrame , coluna1: str, coluna2: str, plot: bool=False) -> pd.DataFrame:
    """Função para agrupar as variaveis categoricas de interesse e retornar um dataframe.
       dataframe : pandas dataframe 
       coluna1 : pandas series : variável categórica do dataframe.
       coluna2 : pandas series : variável categórica do dataframe.        
    """
    dados = dataframe.groupby([coluna1], as_index=False)[coluna2].value_counts().rename(columns=({'count':'frequencia'}))
    dados['porcentagem'] = dataframe.groupby(by=coluna1)[coluna2].value_counts(normalize=True).values*100  

    if plot:
        return dados.sort_values(by=[coluna1,coluna2])
    else:
        return dados.sort_values(by=[coluna1,coluna2]).style.background_gradient(cmap=colormap, high=.5, subset=["porcentagem"])
    
def grpby_difmedia_2amostras(dataframe: pd.DataFrame , coluna1: str, coluna2: str, plot: bool=False) -> pd.DataFrame:
    """Função para agrupar as variaveis categoricas de interesse e retornar um dataframe.
       dataframe : pandas dataframe 
       coluna1 : pandas series : variável categórica do dataframe.
       coluna2 : pandas series : variável categórica do dataframe.        
    """

    dados = dataframe.groupby(by=coluna1, as_index=False)[coluna2].agg(['count','mean'])

    if plot:
        return dados
    else:
        return dados.style.background_gradient(cmap=colormap, high=.5, subset=["mean"])
    
### Gráficos    

def plot_distribuicao(dataframe: pd.DataFrame , coluna: str) -> None:
    """
    Plota um gráfico com a distribuição dos valores de uma determinada coluna
    :param dataframe : pandas dataframe 
    :param coluna: Coluna do dataframe que possue as categorias
    """

    # palette = sns.color_palette(colormap, n_colors=16)

    f, (ax_box, ax_scatter, ax_hist) = plt.subplots(3, sharex=True, gridspec_kw={"height_ratios": (.25, .20, .55)})
    bins = np.histogram_bin_edges(dataframe[coluna], bins='auto')

    sns.boxplot(data=dataframe, x=coluna, meanprops={'marker' : 'D', 'markeredgecolor' : 'black', 'markersize' : 6},
                showmeans=True, showfliers=True, showbox=True, showcaps=True, fill=True, linecolor='k', ax=ax_box)
    sns.stripplot(data=dataframe, x=coluna, jitter=0.3, alpha=0.5, ax=ax_scatter)
    sns.histplot(data=dataframe, x=coluna,  bins=bins, shrink=0.95, stat='density', ax=ax_hist)
    sns.kdeplot(data=dataframe, x=coluna, fill=True, alpha=0.5, ax=ax_hist)

    ax_box.set(yticks=[])
    ax_hist.set(yticks=[])
    ax_scatter.set(yticks=[])
    ax_hist.set(ylabel='')
    ax_hist.set(xlabel=f'Distribuição de {coluna}')

    sns.despine(ax=ax_hist, left=True)
    sns.despine(ax=ax_box, left=True)
    sns.despine(ax=ax_scatter, left=True)

    plt.show() 
   
    return None

def plot_difmedia_2amostras(dataframe: pd.DataFrame, coluna1: str, coluna2: str, xlabel: str=np.nan, title: str=np.nan) -> None:
    """
    Plota um gráfico com as diferenças entre as médias de 2 amostras
    :param dataframe : pandas dataframe 
    :param coluna: Coluna do dataframe que possue as categorias
    :param xlabel: label do eixo X
    :param title: Título do gráfico 
    """
    if pd.isna(xlabel):
        xlabel = coluna1

    if pd.isna(title):
        title = 'Diferença entre as médias de amostras de ' + coluna1

    data = grpby_difmedia_2amostras(dataframe=dataframe, coluna1=coluna1, coluna2=coluna2, plot=True)

    plt.figure(figsize=(8,4))

    ax = sns.barplot(data=data, x=coluna1, y='mean', order=data[coluna1], palette=colormap, hue=coluna1)
    plt.ylabel(f'Média de {coluna2}')
    plt.xlabel(xlabel)
    plt.xticks(rotation=45, fontsize=8)

    for container in ax.containers:
        ax.bar_label(container, labels = [f'{x.get_height():.2f}' for x in container], label_type='center', fontsize=10)

    plt.title(title)
    sns.despine()
    plt.show()
    return None        



def plot_frequencia_cat(dataframe: pd.DataFrame, coluna: str, xlabel: str=np.nan, title: str=np.nan, orient: str='v') -> None:
    """
    Plota um gráfico com as frequências e porcentagens das categorias de uma determinada coluna
    :param dataframe : pandas dataframe 
    :param coluna: Coluna do dataframe que possue as categorias
    :param xlabel: label do eixo X
    :param title: Título do gráfico 
    """
    if pd.isna(xlabel):
        xlabel = coluna

    if pd.isna(title):
        title = 'Porcentagem de ' + coluna

    data = frequencia_cat(dataframe=dataframe, coluna=coluna, plot=True)

    plt.figure(figsize=(8,4))

    if str.lower(orient) == 'v':
        ax = sns.barplot(data=data, x=coluna, y='porcentagem', order=data[coluna], orient=orient, palette=colormap)
        plt.ylabel('%')
        plt.xlabel(xlabel)
        plt.xticks(rotation=45, fontsize=8)

        for container in ax.containers:
            ax.bar_label(container, labels = [f'{x.get_height():.2f}%' for x in container], label_type='center', fontsize=10)

    elif str.lower(orient) == 'h':
        ax = sns.barplot(data=data, x='porcentagem', y=coluna, orient=orient, palette=colormap)
        plt.ylabel(xlabel)
        plt.xlabel('%')

        for container in ax.containers:
            ax.bar_label(container, labels = [f'{x.get_width():.2f}%' for x in container], label_type='center', fontsize=10)

    plt.title(title)
    sns.despine()
    plt.show()
    return None

def plot_relacao_entre_2cat(dataframe: pd.DataFrame, coluna1: str, coluna2: str, xlabel: str=np.nan, title: str=np.nan, orient: str='v') -> None:
    """
    Plota um gráfico com as frequências e porcentagens das categorias de uma determinada coluna
    :param dataframe : pandas dataframe 
    :param coluna1: Coluna do dataframe que possue as categorias
    :param coluna2: Coluna do dataframe que possue as categorias
    :param xlabel: label do eixo X
    :param title: Título do gráfico 
    """
    if pd.isna(xlabel):
        xlabel = coluna1

    if pd.isna(title):
        title = 'Proporção entre ' + coluna1 + ' e ' + coluna2

    data = grpby_2cat(dataframe=dataframe, coluna1=coluna1, coluna2=coluna2, plot=True)

    plt.figure(figsize=(8,4))

    if str.lower(orient) == 'v':
        ax = sns.histplot(data=data, x=coluna1, hue=coluna2,  multiple='stack', palette=colormap, weights='porcentagem', shrink=0.9)
        plt.xticks(rotation=45, fontsize=8)
        ax.set_ylabel('%')
        legend = ax.get_legend()
        legend.set_bbox_to_anchor((1, 1))

        for container in ax.containers:
            ax.bar_label(container, labels = [f'{v.get_height():.2f}%' if v.get_height() > 0 else '' for v in container], label_type='center', fontsize=10)

    elif str.lower(orient) == 'h':
        ax = sns.histplot(data=data, y=coluna1, hue=coluna2,  multiple='stack', palette=colormap, weights='porcentagem', shrink=0.9)
        plt.xticks(rotation=45, fontsize=8)
        ax.set_xlabel('%')
        legend = ax.get_legend()
        legend.set_bbox_to_anchor((1, 1))

        for container in ax.containers:
            ax.bar_label(container, labels = [f'{v.get_width():.2f}%' if v.get_width() > 0 else '' for v in container], label_type='center', fontsize=10)

    plt.title(title)
    sns.despine()
    plt.show()
    return None

def plot_relacao_2variaveis(dataframe: pd.DataFrame, coluna_x: str, coluna_y: str, logistic: bool=False, xlabel: str=np.nan, title: str=np.nan) -> None:

    xlabel = coluna_x if pd.isna(xlabel) else xlabel
    title = 'Relação entre ' + coluna_x + ' e ' + coluna_y if pd.isna(title) else title

    plt.figure(figsize=(8,4))
    ax = sns.regplot(data=dataframe, x=coluna_x, y=coluna_y, color='teal', line_kws=dict(color="darkblue"), logistic=logistic)
    ax.set_ylabel(coluna_y)
    plt.xticks(rotation=45, fontsize=8)       
    plt.title(title)
    sns.despine()
    plt.show()
    return None 






if __name__ == '__main__':
    main()
