import requests
from datetime import datetime, timedelta

API_KEY = ''



def get_publish_info(video_id):
    if video_id == None: return None #Caso o vídeo não exista mais
    else:
        # URL da API de pesquisa de vídeo do YouTube
        url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}'

        # Fazer a solicitação à API
        response = requests.get(url)

        # Verificar se a resposta foi bem-sucedida (código 200)
        if response.status_code == 200:
            data = response.json()

            # Extrair data do vídeo
            published_at = data['items'][0]['snippet']['publishedAt']

           # Converter o timestamp para o fuso horário de Brasília (subtraindo 3 horas)
            published_at_brasilia = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ") - timedelta(hours=3)
            published_at_brasilia = published_at_brasilia.strftime("%Y-%m-%d %H:%M:%S")
            
            # Retorno de data
            return published_at_brasilia
        else:
            print('Erro ao coletar informação de vídeo.')
