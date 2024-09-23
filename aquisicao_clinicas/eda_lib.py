import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
# Biblioteca com funções para Análise Exploratória de Dados (EDA).

class Eda_lib:

    def __init__(self, dataframe: pd.DataFrame, nome: str, colormap: str) -> None:
        self.dataframe: pd.DataFrame = dataframe
        self.colormap: str = colormap
        self.nome: str = nome
        self._linhas: int = self.linhas
        self._colunas: int = self.colunas
        self._palette: plt.colors.ListedColormap = self.palette

    def __str__(self) -> str:
        texto = f'O dataset {self.nome} possui {self.linhas} registros e {self.colunas} colunas.' + '\n' + '------------------------------------------------------------------------' + '\n' + self.dataframe.dtypes.to_string()
        return texto

    @property
    def dataframe(self):
        return self._dataframe
    
    @property
    def palette(self):
        return self._palette
    
    @property
    def colormap(self) -> str:
        return self._colormap
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def linhas(self):
        return self._linhas
    
    @property
    def colunas(self):
        return self._colunas
    
    @dataframe.setter
    def dataframe(self, dataframe: pd.DataFrame):
        if dataframe is None:
            raise ValueError('Falta definir o dataframe')
        else:
            self._dataframe = dataframe
            self._linhas = dataframe.shape[0]
            self._colunas = dataframe.shape[1]
    
    @colormap.setter
    def colormap(self, colormap: str):
        if colormap is None:
            raise ValueError('Falta definir as cores para os gráficos')
        else:
            self._colormap = colormap
            self._palette = sns.color_palette(colormap, n_colors=16)
            sns.set_palette(self._palette)

    @nome.setter
    def nome(self, nome: str):
        if nome is None:
            raise ValueError('Falta definir o nome do dataframe.') 
        else:
            self._nome = nome

    def info(self) -> pd.Series:
        return self.dataframe.dtypes
    
    def valores_ausentes(self) -> pd.DataFrame:
        """
        Verifica e informa a existencia de dados nulos.
        :return: um dataframe contendo as colunas com as respectivas qtdes e percentuais de valores ausentes
        """
        data = self.dataframe.isna().agg(['sum', lambda x : (x.sum() / self.dataframe.shape[0]) * 100]).T.rename(columns={'sum':'valores ausentes','<lambda>':'porcentagem'}).sort_values(by='valores ausentes', ascending=True)[self.dataframe.isna().sum() > 0]
        return data.style.background_gradient(cmap=self.colormap, subset=["porcentagem"])

    def to_datetime(self, colunas: list) -> None:
        """
        Converte determinadas colunas para o tipo de dados (datetime)
        :param colunas: lista de colunas
        :return: informação das colunas com o tipo de dados alterado
        """
        for col in colunas:
            self.dataframe[col] = pd.to_datetime(self.dataframe[col])

        return print(self.dataframe[colunas].info())

    # função para exibir as frequencias das variaveis categoricas
    def frequencia_cat(self, coluna: str) -> pd.DataFrame:
        """
        Exibe as frequências e porcentagens das categorias de uma determinada coluna
        :param coluna: Coluna do dataframe que possue as categorias
        :return: Um dataframe com as informações     
        """
        data = self.dataframe[coluna].agg(['value_counts',lambda x : (x.value_counts() / self.dataframe.shape[0])*100]).reset_index().rename(columns={'index':coluna,'value_counts':'frequencia', '<lambda>':'porcentagem'}).sort_values(by='porcentagem', ascending=True)
        return data.style.background_gradient(cmap=self.colormap, high=.5, subset=["porcentagem"])     

    def _frequencia_cat(self, coluna: str) -> pd.DataFrame:
        data = self.dataframe[coluna].agg(['value_counts',lambda x : (x.value_counts() / self.dataframe.shape[0])*100]).reset_index().rename(columns={'index':coluna,'value_counts':'frequencia', '<lambda>':'porcentagem'})
        return data.sort_values(by='porcentagem', ascending=True)
     
    def resumo_estatistico(self, coluna: str) -> None:
        """
        Exibe um resumo estatístico de uma determinada coluna
        :param coluna: Coluna do dataframe
        :return: Um dataframe com as informações estatísticas da coluna 
        """
        def li(x):
            q1 = x.quantile(.25)
            q3 = x.quantile(.75)
            li = q1 - 1.5 * (q3-q1)
            return li

        def ls(x):
            q1 = x.quantile(.25)
            q3 = x.quantile(.75)
            ls = q3 + 1.5 * (q3-q1)
            return ls

        def q25(x):
            return x.quantile(.25)

        def q75(x):
            return x.quantile(.75)        
        
        print('*************************** Resumo Estatístico **************************')
        print('')
        print(f'A variável {coluna} possui {self.dataframe[coluna].count()} registros.')
        print('')
        print('--- Medidas Tendencia Central -------------------------------------------')
        # Medidas Tendencia Central
        display(self.dataframe[coluna].agg({'Média':'mean', 'Mediana':'median'}).to_frame().apply(lambda s: s.apply('{0:.3f}'.format)).T)
        # print('-------------------------------------------------------------------------')
        # print('')
        print('--- Medidas de Dispersão ------------------------------------------------')
        # Medidas de dispersão
        display(self.dataframe[coluna].agg({'dp':'std','var':'var','CV%':lambda x: (x.std()/x.mean())*100
                                    , 'Skew': lambda x: x.skew(), 'min':'min', 'max':'max', 'Alcance':lambda x: (x.max() - x.min())}).to_frame().apply(lambda s: s.apply('{0:.3f}'.format)).T)
        # print('-------------------------------------------------------------------------')
        # print('')
        print('--- Medidas Separatrizes ------------------------------------------------')
        # Medidas Separatrizes
        display(self.dataframe[coluna].agg({'25%':q25, '50%': 'median', '75%':q75, 'Limite inferior':li, 'Limite Superior':ls}).to_frame().T)
        # print('-------------------------------------------------------------------------')   

        return None


    def plot_distribuicao(self, coluna: str) -> None:
        """
        Plota um gráfico com a distribuição dos valores de uma determinada coluna
        :param coluna: Coluna do dataframe que possue as categorias
        """
   
        f, (ax_box, ax_scatter, ax_hist) = plt.subplots(3, sharex=True, gridspec_kw={"height_ratios": (.25, .20, .55)})
        bins = np.histogram_bin_edges(self.dataframe[coluna], bins='auto')

        sns.boxplot(data=self.dataframe, x=coluna, meanprops={'marker' : 'D', 'markeredgecolor' : 'black', 'markersize' : 6},
                    showmeans=True, showfliers=True, showbox=True, showcaps=True, fill=True, linecolor='k', ax=ax_box)
        sns.stripplot(data=self.dataframe, x=coluna, jitter=0.3, alpha=0.5, ax=ax_scatter)
        sns.histplot(data=self.dataframe, x=coluna,  bins=bins, shrink=0.95, stat='density', ax=ax_hist)
        sns.kdeplot(data=self.dataframe, x=coluna, fill=True, alpha=0.5, ax=ax_hist)

        ax_box.set(yticks=[])
        ax_hist.set(yticks=[])
        ax_scatter.set(yticks=[])
        ax_hist.set(ylabel='')
        ax_hist.set(xlabel=f'Distribuição de {coluna}')

        sns.despine(ax=ax_hist, left=True)
        sns.despine(ax=ax_box, left=True)
        sns.despine(ax=ax_scatter, left=True)

        plt.show() 

        self.resumo_estatistico(coluna=coluna)
        
        return None
   
    def plot_frequencia_cat(self, coluna: str, xlabel: str=np.nan, title: str=np.nan, orient: str='v') -> None:
        """
        Plota um gráfico com as frequências e porcentagens das categorias de uma determinada coluna
        :param coluna: Coluna do dataframe que possue as categorias
        :param xlabel: label do eixo X
        :param title: Título do gráfico 
        """
        if pd.isna(xlabel):
            xlabel = coluna

        if pd.isna(title):
            title = 'Porcentagem de ' + coluna

        data = self._frequencia_cat(coluna)

        plt.figure(figsize=(8,4))

        if str.lower(orient) == 'v':
            ax = sns.barplot(data=data, x=coluna, y='porcentagem', order=data[coluna], orient=orient, palette=self.palette)
            plt.ylabel('%')
            plt.xlabel(xlabel)
            plt.xticks(rotation=45, fontsize=8)

            for container in ax.containers:
                ax.bar_label(container, labels = [f'{x.get_height():.2f}%' for x in container])

        elif str.lower(orient) == 'h':
            ax = sns.barplot(data=data, x='porcentagem', y=coluna, orient=orient, palette=self.palette)
            plt.ylabel(xlabel)
            plt.xlabel('%')

            for container in ax.containers:
                ax.bar_label(container, labels = [f'{x.get_width():.2f}%' for x in container])
    
        plt.title(title)
        sns.despine()
        plt.show()
        return None
