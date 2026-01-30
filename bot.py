import os
import requests
import telebot

# Recupera as chaves
TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
API_CRYPTOPANIC = os.environ.get('CRYPTOPANIC_KEY')

bot = telebot.TeleBot(TOKEN_TELEGRAM)
GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'DOGE', 'WHALE', 'BALEIA', 'CAMPAIGN', 'FED', 'LAUNCH', 'LISTING', 'BTC']

def buscar_noticias_inovadoras():
    # TESTE DE DIAGNÓSTICO
    if not API_CRYPTOPANIC:
        return "❌ ERRO CRÍTICO: A chave da API não foi carregada. Verifique o arquivo YAML ou os Secrets."
    
    print(f"🔑 Chave detectada (início): {API_CRYPTOPANIC[:4]}...") # Mostra só o começo para confirmar

    # URL Base
    url = "https://cryptopanic.com/api/v1/posts/"
    
    # Parâmetros separados (mais seguro)
    params = {
        "auth_token": API_CRYPTOPANIC,
        "public": "true",
        "filter": "hot",
        "regions": "en" # Foca em notícias globais em inglês (maior volume)
    }

    # Finge ser um navegador Chrome para evitar erro 404/403
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, params=params, headers=headers)
    
    # Se der erro, retorna o motivo exato
    if response.status_code != 200:
        return f"❌ Erro na API: {response.status_code} - Tentativa de acesso bloqueada ou URL inválida."

    try:
        data = response.json()
    except:
        return "❌ Erro ao ler JSON. O site pode estar fora do ar."

    destaques = []
    geral = []

    # Processa os resultados
    if 'results' in data:
        for post in data['results'][:15]:
            titulo = post['title'].upper()
            url_noticia = post['url']
            
            # Verifica gatilhos
            if any(keyword in titulo for keyword in GATILHOS):
                destaques.append(f"🔥 *ALERTA:* {titulo}\n🔗 [Link]({url_noticia})")
            else:
                geral.append(f"🔹 {titulo}")
    
    if not destaques and not geral:
        return "Nenhuma notícia relevante encontrada no momento."

    msg = "🚀 *RESUMO DE MERCADO 24H*\n\n"
    if destaques:
        msg += "🚨 *IMPACTO IMEDIATO:*\n" + "\n\n".join(destaques) + "\n\n"
    if geral:
        msg += "📰 *RADAR GERAL:*\n" + "\n".join(geral[:5])
        
    return msg

def enviar():
    try:
        conteudo = buscar_noticias_inovadoras()
        print("Tentando enviar mensagem...")
        bot.send_message(CHAT_ID, conteudo, parse_mode='Markdown', disable_web_page_preview=True)
        print("Mensagem enviada com sucesso!")
    except Exception as e:
        print(f"Erro no envio Telegram: {e}")

if __name__ == "__main__":
    enviar()
