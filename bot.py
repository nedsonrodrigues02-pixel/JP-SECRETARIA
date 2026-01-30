import os
import requests
import telebot

# Configurações via GitHub Secrets
TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
API_CRYPTOPANIC = os.environ.get('CRYPTOPANIC_KEY')

bot = telebot.TeleBot(TOKEN_TELEGRAM)

# Palavras-chave que indicam possível alavancagem ou impacto de baleias/influenciadores
GATILHOS = ['trump', 'musk', 'elon', 'doge', 'whale', 'baleia', 'campaign', 'fed', 'launch', 'listing']

def buscar_noticias_inovadoras():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={API_CRYPTOPANIC}&public=true&filter=hot"
    response = requests.get(url).json()
    
    destaques = []
    geral = []

    for post in response['results'][:15]: # Analisa as 15 mais quentes
        titulo = post['title'].upper()
        url_noticia = post['url']
        
        # Verifica se a notícia contém algum dos nossos gatilhos (Trump, Musk, etc)
        if any(keyword.upper() in titulo for keyword in GATILHOS):
            destaques.append(f"🔥 *ALERTA DE IMPACTO:* \n{titulo}\n🔗 [Link]({url_noticia})")
        else:
            geral.append(f"🔹 {titulo}")

    # Montagem da mensagem
    mensagem_final = "🚀 *MONITORAMENTO 24H - MERCADO CRIPTO*\n\n"
    
    if destaques:
        mensagem_final += "🚨 *MOVIMENTAÇÕES IMPORTANTES:*\n" + "\n\n".join(destaques) + "\n\n"
    
    if geral:
        mensagem_final += "📰 *OUTRAS NOTÍCIAS RECENTES:*\n" + "\n".join(geral[:5])
        
    return mensagem_final

def enviar():
    try:
        conteudo = buscar_noticias_inovadoras()
        bot.send_message(CHAT_ID, conteudo, parse_mode='Markdown', disable_web_page_preview=True)
        print("Relatório inovador enviado!")
    except Exception as e:
        print(f"Erro ao enviar: {e}")

if __name__ == "__main__":
    enviar()
