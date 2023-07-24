from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Define as opções do Chrome para modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")


def webscrapping_yt(d1,d2):
    # Formato da data 'YYYY-MM-DD'
    datinicio =  str(d1.replace("-", ""))
    datfim =  str(d2.replace("-", ""))

    # Inicializa o navegador Chrome
    driver = webdriver.Chrome(options=chrome_options)

    # URL da página
    url = f'https://charts.youtube.com/charts/TopSongs/br/{datinicio}-{datfim}?hl=pt'

    try:
        # Abre a página
        driver.get(url)

        # Espera até que o botão esteja presente na página e visível
        div_xpath = "/html/body/ytmc-app/div[3]/ytmc-charts/div[2]/ytmc-chart-table/div/div"
        wait = WebDriverWait(driver, 10)
        div = wait.until(EC.element_to_be_clickable((By.XPATH, div_xpath)))

    except:
        print("Erro ao encontrar Playlist")

    # Extrai o conteúdo da div
    div_content = div.get_attribute('innerHTML')

    # Fechar o driver do Selenium
    driver.quit()

    # Processar o conteúdo usando Beautiful Soup para obter os dados desejados
    soup = BeautifulSoup(div_content, 'html.parser')

    classificacao = []
    classificacao_sp = []
    titulo = []
    artistas = []
    idvideo = []
    semanas_charts = []
    var_views = []
    views =[]


    # Exemplo de como extrair os títulos e artistas da tabela dentro da div
    for row in soup.find_all('div', class_='chart-table-row style-scope ytmc-chart-table'):

        #Classificação
        classificacao_text = row.find('div', class_='rank style-scope ytmc-chart-table').get_text()
        classificacao.append(classificacao_text)

        #Classificação Semana Passada
        classificacao_sp_text = row.find('div', class_='previous-rank style-scope ytmc-chart-table').get_text()
        classificacao_sp_text = classificacao_sp_text.replace("\nsemana passada #","").replace("\n\n\n","")
        if classificacao_sp_text == '--': classificacao_sp_text = "-"
        classificacao_sp.append(classificacao_sp_text)
        
        #Título
        titulo_text = row.find('span', class_='ytmc-ellipsis-text style-scope').get_text()
        titulo.append(titulo_text) 


        artists_list = row.find('div', class_='ytmc-artists-list-container style-scope ytmc-artists-list')

        if artists_list:
            artistas_musica = []  # Inicialize uma lista temporária para cada música

            for element in artists_list.find_all('span'):
                artistas_musica.append(element.get_text())
            #Salvando Tupla
            artistas.append(tuple(artistas_musica))    

        #idVideo
        a = str(row)

        inicio_str = a.find('https://www.youtube.com/watch?v=')
        fim_str = a.find('","target":"TARGET_NEW_WINDOW"')

        # Verificar se encontrou as duas substrings desejadas
        if inicio_str != -1 and fim_str != -1:
            # Extrair a URL completa
            valor_apos_watch = a[inicio_str:fim_str]

            idvideo.append(valor_apos_watch)
        else:
            # Caso o vídeo não exista mais
            idvideo.append(None)



        #Semanas_em_Charts
        semanas_text = row.find('div', class_='chart-period style-scope ytmc-chart-table').get_text()
        semanas_text = semanas_text.replace(" semanas\n\n\n", "").replace("\n", "").replace(" semana","")
        semanas_charts.append(semanas_text) 

        #Var_Views
        var_views_text = row.find('div', class_='views-change style-scope ytmc-chart-table').get_text()
        var_views_text = var_views_text.replace("%\n\n\n", "").replace("\n", "")
        if var_views_text == '--': var_views_text = 0
        var_views.append(var_views_text) 

        #Views
        views_text = row.find('div', class_='views style-scope ytmc-chart-table').get_text()
        views_text = views_text.replace("M", "").replace("\n", "")
        views.append(views_text)

    dados = {
        'classificacao': classificacao,
        'semanaPassada': classificacao_sp,
        'titulo': titulo,
        'artistas': artistas,
        'idVideo': idvideo,
        'semanas': semanas_charts,
        'varViews': var_views,
        'views': views,
        'iniSemana': d1,
        'fimSemana': d2
    }

    df = pd.DataFrame(dados)
    
    return df
