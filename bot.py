import os
import requests
import telebot
import json

# --- CONFIGURAÇÕES ---
TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
API_CRYPTOPANIC = os.environ.get('CRYPTOPANIC_KEY', '').strip()

bot = telebot.TeleBot(TOKEN_TELEGRAM)

# --- GATILHOS DA ZUEIRA ---
GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'BLACKROCK', 'ETF', 'FED', 'BTC', 'SOL', 'PEPE', 'RWA', 'AI', 'WHALE']

def buscar_noticias():
    print("----- RODANDO A JP SAFADA (V2) -----")
    
    # URL DE DEVELOPER (Corrigida)
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
        
        if response.status_code != 200:
            print(f"⚠️ Erro API: {response.status_code} - {response.text[:100]}")
            return f"Chefinho, a porta tá fechada (Erro {response.status_code})."

        data = response.json()
        print("✅ Conexão V2 estabelecida!")

        # --- DIAGNÓSTICO DE CHAVES (Pra gente saber o nome certo se der erro) ---
        if 'results' in data and len(data['results']) > 0:
            primeiro_post = data['results'][0]
            print(f"🔍 Chaves encontradas no post: {list(primeiro_post.keys())}")

    except Exception as e:
        print(f"❌ Erro de Conexão: {e}")
        return f"Chefinho, tropecei no cabo: {e}"

    # --- PROCESSAMENTO ---
    destaques = []
    
    if 'results' in data:
        for post in data['results'][:15]:
            titulo = post.get('title', 'Sem Título')
            
            # --- CORREÇÃO DO ERRO DE URL ---
            # Tenta pegar 'url'. Se não tiver, tenta montar com 'slug'.
            if 'url' in post:
                url_noticia = post['url']
            elif 'slug' in post:
                url_noticia = f"https://cryptopanic.com/news/{post['slug']}"
            else:
                url_noticia = "https://cryptopanic.com" # Link genérico pra não travar

            # Verifica gatilhos
            for gatilho in GATILHOS:
                if gatilho in titulo.upper():
                    destaques.append(f"🔥 *{gatilho} NA ÁREA:*\n{titulo}\n🔗 [Vê isso aqui]({url_noticia})")
                    break
    
    if not destaques:
        return "Oi chefinho, aqui é a JP SAFADA molestada.\nNão tem fofoca boa agora não, mercado tá uma uva. 🍇"
        
    cabecalho = "Oi chefinho aqui sou eu a JP SAFADA molestada e trago notícias 💅🏻\n\n"
    corpo = "\n\n".join(destaques)
    
    return cabecalho + corpo

if __name__ == "__main__":
    try:
        msg = buscar_noticias()
        bot.send_message(CHAT_ID, msg, parse_mode='Markdown', disable_web_page_preview=True)
        print("Mensagem da JP enviada.")
    except Exception as e:
        print(f"Erro no Telegram: {e}")
