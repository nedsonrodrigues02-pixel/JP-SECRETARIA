import os
import requests
import telebot
import json

# --- CONFIGURAÇÕES ---
TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
key_raw = os.environ.get('CRYPTOPANIC_KEY', '')
API_CRYPTOPANIC = key_raw.strip()

bot = telebot.TeleBot(TOKEN_TELEGRAM)

# --- GATILHOS 2026 ---
GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'BLACKROCK', 'ETF', 'FED', 'BTC', 'SOL', 'PEPE', 'RWA', 'AI', 'WHALE']

def buscar_noticias():
    print("----- INICIANDO CONEXÃO -----")
    
    # 1. URL sem a barra no final (Correção para erro 404)
    url = "https://cryptopanic.com/api/v1/posts" 
    
    # 2. Montagem segura dos parâmetros
    params = {
        "auth_token": API_CRYPTOPANIC,
        "public": "true",
        "filter": "hot",
        "kind": "news"
    }

    # 3. Headers completos para simular um PC real (Evita bloqueio)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    print(f"🔄 Acessando: {url} (Token final: ...{API_CRYPTOPANIC[-4:] if API_CRYPTOPANIC else 'NULO'})")

    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        print(f"📡 Status Code: {response.status_code}")

        # Se der erro, mostra o que o site respondeu
        if response.status_code != 200:
            print(f"⚠️ Erro na resposta: {response.text[:200]}")
            return f"Erro na API ({response.status_code}). Veja o log."

        data = response.json()
        print("✅ Dados recebidos com sucesso!")

    except Exception as e:
        print(f"❌ Erro Crítico: {e}")
        return f"Erro técnico: {e}"

    # --- FILTRAGEM ---
    destaques = []
    
    if 'results' in data:
        for post in data['results'][:15]:
            titulo = post['title']
            url_noticia = post['url']
            
            # Verifica gatilhos (case insensitive)
            for gatilho in GATILHOS:
                if gatilho in titulo.upper():
                    destaques.append(f"🔥 *{gatilho} DETECTADO:*\n{titulo}\n🔗 [Ler]({url_noticia})")
                    break
    
    if not destaques:
        return "Nenhuma 'Bomba' de mercado detectada agora."
        
    return "🚨 *ALERTA CRIPTO 2026:*\n\n" + "\n\n".join(destaques)

if __name__ == "__main__":
    try:
        msg = buscar_noticias()
        bot.send_message(CHAT_ID, msg, parse_mode='Markdown', disable_web_page_preview=True)
        print("Mensagem enviada.")
    except Exception as e:
        print(f"Erro Telegram: {e}")
