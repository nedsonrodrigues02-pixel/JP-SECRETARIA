import os
import requests
import telebot

TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
API_CRYPTOPANIC = os.environ.get('CRYPTOPANIC_KEY')

bot = telebot.TeleBot(TOKEN_TELEGRAM)
GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'DOGE', 'WHALE', 'BALEIA', 'CAMPAIGN', 'FED', 'LAUNCH', 'LISTING']

def buscar_noticias_inovadoras():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={API_CRYPTOPANIC}&public=true&filter=hot"
    response = requests.get(url)
    
    # Verifica se a API retornou erro (ex: 401 Unauthorized)
    if response.status_code != 200:
        return f"❌ Erro na API CryptoPanic: Status {response.status_code}. Verifique sua chave!"

    try:
        data = response.json()
    except Exception:
        return "❌ Erro ao processar JSON da API."

    destaques = []
    geral = []

    for post in data.get('results', [])[:15]:
        titulo = post['title'].upper()
        url_noticia = post['url']
        
        if any(keyword in titulo for keyword in GATILHOS):
            destaques.append(f"🔥 *ALERTA:* {titulo}\n🔗 [Link]({url_noticia})")
        else:
            geral.append(f"🔹 {titulo}")

    if not destaques and not geral:
        return "Nenhuma notícia encontrada no momento."

    msg = "🚀 *MONITORAMENTO CRIPTO*\n\n"
    if destaques:
        msg += "🚨 *IMPACTO:*\n" + "\n\n".join(destaques) + "\n\n"
    if geral:
        msg += "📰 *RECENTES:*\n" + "\n".join(geral[:5])
        
    return msg

def enviar():
    try:
        conteudo = buscar_noticias_inovadoras()
        bot.send_message(CHAT_ID, conteudo, parse_mode='Markdown', disable_web_page_preview=True)
    except Exception as e:
        print(f"Erro no Telegram: {e}")

if __name__ == "__main__":
    enviar()
