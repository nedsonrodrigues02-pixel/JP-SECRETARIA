import os
import requests
import telebot
import json

# --- CONFIGURAÇÕES ---
TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
API_CRYPTOPANIC = os.environ.get('CRYPTOPANIC_KEY', '').strip()

bot = telebot.TeleBot(TOKEN_TELEGRAM)

# --- GATILHOS 2026 ---
GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'BLACKROCK', 'ETF', 'FED', 'BTC', 'SOL', 'PEPE', 'RWA', 'AI', 'WHALE']

def buscar_noticias():
    print("----- INICIANDO CONEXÃO (NÍVEL DEVELOPER) -----")
    
    # --- CORREÇÃO FINAL AQUI ---
    # Sua conta é Developer, então a URL base é v2 e não v1
    url = "https://cryptopanic.com/api/developer/v2/posts/" 
    
    params = {
        "auth_token": API_CRYPTOPANIC,
        "public": "true",
        "filter": "hot",
        "kind": "news"
    }

    # Headers para evitar bloqueio
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"🔄 Acessando: {url}")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"⚠️ Erro na resposta: {response.text[:200]}")
            return f"Erro na API ({response.status_code})."

        data = response.json()
        print("✅ Dados recebidos com sucesso!")

    except Exception as e:
        print(f"❌ Erro Crítico: {e}")
        return f"Erro técnico: {e}"

    # --- PROCESSAMENTO ---
    destaques = []
    
    if 'results' in data:
        for post in data['results'][:15]:
            titulo = post['title']
            url_noticia = post['url']
            
            # Verifica gatilhos
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
