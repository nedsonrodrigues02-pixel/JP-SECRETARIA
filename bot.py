import os
import requests
import telebot

# --- CONFIGURAÇÕES ---
TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
API_CRYPTOPANIC = os.environ.get('CRYPTOPANIC_KEY')

bot = telebot.TeleBot(TOKEN_TELEGRAM)

# --- SEUS GATILHOS ---
GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'BLACKROCK', 'ETF', 'FED', 'BTC', 'SOL', 'PEPE', 'WIF', 'RWA', 'AI']

def diagnostico_e_busca():
    print("----- INICIANDO DIAGNÓSTICO -----")
    
    # 1. Verifica se a chave existe dentro do ambiente do GitHub
    if not API_CRYPTOPANIC:
        print("❌ ERRO GRAVE: O Python não encontrou a chave 'CRYPTOPANIC_KEY'.")
        print("👉 O problema está no arquivo YAML ou no nome do Secret nas configurações.")
        return "Erro interno de configuração (Chave ausente)."
    
    # Mostra os primeiros 4 digitos da chave pra confirmar se leu (segurança)
    print(f"✅ Chave carregada. Início: {API_CRYPTOPANIC[:4]}***")
    
    # 2. Tenta a requisição de forma mais limpa (usando params)
    url = "https://cryptopanic.com/api/v1/posts/"
    
    params = {
        "auth_token": API_CRYPTOPANIC.strip(),
        "public": "true",
        "filter": "hot",
        "kind": "news"
    }

    # Headers simples
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    print(f"🔄 Tentando conectar em: {url}")
    
    try:
        response = requests.get(url, params=params, headers=headers)
        
        print(f"📡 Status Code recebido: {response.status_code}")
        
        # Se der erro 404 ou outro, vamos ver o que o site respondeu (HTML ou erro)
        if response.status_code != 200:
            print(f"⚠️ Corpo da resposta (Erro): {response.text[:200]}") # Imprime o erro real
            return f"Erro na API: {response.status_code}"

        data = response.json()
        print("✅ Conexão bem sucedida! JSON recebido.")
        
    except Exception as e:
        print(f"❌ Exceção Python: {e}")
        return f"Erro técnico: {e}"

    # --- PROCESSAMENTO (Igual ao anterior) ---
    destaques = []
    
    if 'results' in data:
        for post in data['results'][:15]:
            titulo = post['title'].upper()
            url_noticia = post['url']
            
            for gatilho in GATILHOS:
                if gatilho in titulo:
                    destaques.append(f"🔥 *{gatilho}:* {post['title']}\n🔗 [Ler]({url_noticia})")
                    break
    
    if not destaques:
        return "Monitoramento ativo. Nenhuma 'bomba' detectada agora."
        
    return "🚨 *ALERTA 2026:*\n\n" + "\n\n".join(destaques)

if __name__ == "__main__":
    msg = diagnostico_e_busca()
    try:
        bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
        print("Mensagem enviada.")
    except Exception as e:
        print(f"Erro Telegram: {e}")
