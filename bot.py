import os
import requests
import telebot
import random
from deep_translator import GoogleTranslator

# --- CONFIGURAÇÕES ---
TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
API_CRYPTOPANIC = os.environ.get('CRYPTOPANIC_KEY', '').strip()

bot = telebot.TeleBot(TOKEN_TELEGRAM)
tradutor = GoogleTranslator(source='auto', target='pt')

# --- GATILHOS ---
GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'BLACKROCK', 'ETF', 'FED', 'BTC', 'SOL', 'PEPE', 'RWA', 'AI', 'WHALE', 'DOGE', 'XRP']

# --- BANCO DE IMAGENS DA JP (Para ilustrar o post) ---
IMAGENS_ZUEIRA = [
    "https://media1.giphy.com/media/trN9df5NmUOqCx21jo/giphy.gif", # Bull run
    "https://i.pinimg.com/originals/7d/44/1f/7d441fa14580436d10c5383505c24949.gif", # Matrix rain
    "https://media.giphy.com/media/7FBY7h5Psqd20/giphy.gif", # Money
    "https://i.gifer.com/origin/f5/f5baef4b6b6677020ab8d091a78a6345_w200.gif", # Stonks
    "https://media.giphy.com/media/JtBZm3Getg3dqxK0zP/giphy.gif", # Crypto falling/rising
    "https://media.tenor.com/images/1c0155b486e929f6498ba4b3b02ba547/tenor.gif" # Doge
]

def buscar_noticias():
    print("----- RODANDO A JP SAFADA (V2.5 - TRADUÇÃO) -----")
    
    url = "https://cryptopanic.com/api/developer/v2/posts/" 
    
    params = {
        "auth_token": API_CRYPTOPANIC,
        "public": "true",
        "filter": "hot",
        "kind": "news"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None, f"Chefinho, deu ruim na conexão: {e}"

    destaques = []
    
    if 'results' in data:
        for post in data['results'][:10]: # Analisa as 10 mais quentes
            titulo_en = post.get('title', '')
            
            # Tenta pegar url ou slug
            if 'url' in post:
                link = post['url']
            elif 'slug' in post:
                link = f"https://cryptopanic.com/news/{post['slug']}"
            else:
                link = "https://cryptopanic.com"

            # Fonte da notícia (Domain)
            fonte = post.get('domain', 'Fonte desconhecida')

            # Verifica se tem gatilho
            encontrou = False
            for gatilho in GATILHOS:
                if gatilho in titulo_en.upper():
                    encontrou = True
                    # --- TRADUÇÃO DO TÍTULO ---
                    try:
                        titulo_pt = tradutor.translate(titulo_en)
                    except:
                        titulo_pt = titulo_en # Se falhar, usa inglês mesmo

                    # Formatação Bonita
                    texto_formatado = (
                        f"🔥 *{gatilho} DETECTADO*\n"
                        f"🇧🇷 *{titulo_pt}*\n"
                        f"🇺🇸 _{titulo_en}_\n"
                        f"🗞️ Fonte: {fonte}\n"
                        f"🔗 [Ler matéria completa]({link})"
                    )
                    destaques.append(texto_formatado)
                    break 
    
    # Se não tiver destaques, não manda nada (ou manda aviso)
    if not destaques:
        return None, "Nada de relevante agora, chefinho."

    # Monta a mensagem final
    cabecalho = "Oi chefinho aqui sou eu a JP SAFADA molestada e trago notícias 💅🏻\n\n"
    corpo = "\n\n━━━━━━━━━━━━━━━━━━━━\n\n".join(destaques)
    msg_final = cabecalho + corpo
    
    # Escolhe uma imagem aleatória para ilustrar
    imagem = random.choice(IMAGENS_ZUEIRA)
    
    return imagem, msg_final

if __name__ == "__main__":
    try:
        imagem, texto = buscar_noticias()
        
        if imagem and texto and "Nada de relevante" not in texto:
            # Envia como FOTO com a legenda (caption)
            bot.send_photo(CHAT_ID, photo=imagem, caption=texto, parse_mode='Markdown')
            print("Mensagem com foto enviada!")
        elif texto:
            # Se não tiver foto ou for msg de erro, envia só texto
            bot.send_message(CHAT_ID, texto)
            print("Mensagem de texto enviada.")
            
    except Exception as e:
        print(f"Erro no Telegram: {e}")
