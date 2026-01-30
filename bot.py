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

# --- BANCO DE IMAGENS ATUALIZADO (Links mais estáveis) ---
IMAGENS_ZUEIRA = [
    "https://media.tenor.com/images/1c0155b486e929f6498ba4b3b02ba547/tenor.gif", # Doge
    "https://i.pinimg.com/originals/7d/44/1f/7d441fa14580436d10c5383505c24949.gif", # Matrix
    "https://media1.giphy.com/media/trN9df5NmUOqCx21jo/giphy.gif", # Bull
    "https://media.giphy.com/media/7FBY7h5Psqd20/giphy.gif", # Money
    # Adicionei imagens estáticas também caso os GIFs falhem
    "https://cdn.pixabay.com/photo/2018/01/18/07/31/bitcoin-3089728_1280.jpg",
    "https://cdn.pixabay.com/photo/2021/05/09/13/10/finance-6240949_1280.jpg"
]

def buscar_noticias():
    print("----- RODANDO A JP SAFADA (V3.0 - BLINDADA) -----")
    
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
        return None, f"Chefinho, deu ruim na conexão: {e}"

    destaques = []
    
    if 'results' in data:
        for post in data['results'][:10]: 
            titulo_en = post.get('title', '')
            
            if 'url' in post:
                link = post['url']
            elif 'slug' in post:
                link = f"https://cryptopanic.com/news/{post['slug']}"
            else:
                link = "https://cryptopanic.com"

            fonte = post.get('domain', 'Fonte desconhecida')

            for gatilho in GATILHOS:
                if gatilho in titulo_en.upper():
                    # --- TRADUÇÃO SEGURA ---
                    try:
                        titulo_pt = tradutor.translate(titulo_en)
                    except:
                        titulo_pt = titulo_en 

                    texto_formatado = (
                        f"🔥 *{gatilho} DETECTADO*\n"
                        f"🇧🇷 *{titulo_pt}*\n"
                        f"🇺🇸 _{titulo_en}_\n"
                        f"🗞️ Fonte: {fonte}\n"
                        f"🔗 [Ler matéria completa]({link})"
                    )
                    destaques.append(texto_formatado)
                    break 
    
    if not destaques:
        return None, "Nada de relevante agora, chefinho."

    cabecalho = "Oi chefinho aqui sou eu a JP SAFADA molestada e trago notícias 💅🏻\n\n"
    corpo = "\n\n━━━━━━━━━━━━━━━━━━━━\n\n".join(destaques)
    msg_final = cabecalho + corpo
    
    imagem = random.choice(IMAGENS_ZUEIRA)
    
    return imagem, msg_final

if __name__ == "__main__":
    try:
        imagem, texto = buscar_noticias()
        
        if imagem and texto and "Nada de relevante" not in texto:
            try:
                # TENTA ENVIAR A FOTO
                print(f"Tentando enviar imagem: {imagem}")
                bot.send_photo(CHAT_ID, photo=imagem, caption=texto, parse_mode='Markdown')
                print("✅ Sucesso: Foto enviada!")
            except Exception as e_foto:
                # SE A FOTO FALHAR, ENVIA SÓ O TEXTO (FALLBACK)
                print(f"⚠️ Erro na imagem ({e_foto}). Enviando apenas texto...")
                bot.send_message(CHAT_ID, texto, parse_mode='Markdown')
                print("✅ Sucesso: Texto enviado (modo de segurança).")
        
        elif texto:
            bot.send_message(CHAT_ID, texto)
            
    except Exception as e:
        print(f"❌ Erro Crítico Telegram: {e}")
