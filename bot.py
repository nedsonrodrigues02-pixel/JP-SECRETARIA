import os
import requests
import telebot

# --- CONFIGURAÇÕES E CHAVES ---
TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
key_raw = os.environ.get('CRYPTOPANIC_KEY', '')
API_CRYPTOPANIC = key_raw.strip() # Remove espaços invisíveis para evitar erro 404

bot = telebot.TeleBot(TOKEN_TELEGRAM)

# --- PACK DE GATILHOS INOVADORES 2026 ---
# O bot vai buscar qualquer notícia que contenha essas palavras (em inglês ou pt)
GATILHOS = [
    # Influenciadores & Figuras
    'TRUMP', 'MUSK', 'ELON', 'SAYLOR', 'VITALIK', 'CZ',
    
    # Institucional & Regulatório
    'BLACKROCK', 'VANGUARD', 'FIDELITY', 'ETF', 'SEC', 'FED', 'POWELL', 'CHINA',
    
    # Narrativas Fortes de 2026
    'AI', 'GPT', 'RWA', 'TOKENIZATION', 'DEPIN', 'LAYER 2', 'ZK', 'GAMING',
    
    # Ação de Mercado & Baleias
    'WHALE', 'BALEIA', 'BUYING', 'ACCUMULATION', 'ATH', 'BREAKOUT', 'PUMP', 
    'BURN', 'QUEIMA', 'AIRDROP', 'LAUNCH', 'LISTING', 'MAINNET',
    
    # Moedas Chave (Adicione outras se quiser)
    'BTC', 'ETH', 'SOL', 'XRP', 'DOGE', 'PEPE'
]

def buscar_noticias_quentes():
    # URL montada para pegar notícias "HOT" (Tendência)
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={API_CRYPTOPANIC}&public=true&filter=hot"
    
    print(f"🔄 Buscando notícias quentes...")

    # Headers para evitar bloqueio (Erro 404/403)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        return f"❌ Erro de conexão: {e}"
    
    if response.status_code != 200:
        return f"❌ Erro na API CryptoPanic: {response.status_code}"

    try:
        data = response.json()
    except:
        return "❌ Erro ao processar dados da API."

    destaques = []
    radar = []

    if 'results' in data:
        # Analisa as 20 notícias mais quentes do momento
        for post in data['results'][:20]:
            titulo = post['title']
            titulo_upper = titulo.upper() # Converte pra maiúsculo pra comparar
            url_noticia = post['url']
            
            # Moedas mencionadas (se a API fornecer)
            moedas = ""
            if 'currencies' in post:
                codigos = [c['code'] for c in post['currencies']]
                if codigos:
                    moedas = f" | 🪙 {', '.join(codigos)}"

            # Lógica de Filtro: Verifica se tem algum gatilho no título
            encontrou_gatilho = False
            for gatilho in GATILHOS:
                if gatilho in titulo_upper:
                    # Formata a mensagem com destaque
                    destaques.append(f"🔥 *{gatilho} DETECTADO:*\n{titulo}{moedas}\n🔗 [Ler Agora]({url_noticia})")
                    encontrou_gatilho = True
                    break # Para de procurar gatilhos nessa notícia e vai pra próxima
            
            # Se não for destaque, mas for notícia Hot, joga pro Radar (limite de 3)
            if not encontrou_gatilho and len(radar) < 3:
                radar.append(f"• {titulo}")
    
    if not destaques and not radar:
        return "Sem movimentações relevantes no radar agora."

    # Montagem do Relatório
    msg = "🛰️ *RADAR CRIPTO 2026 - 2H*\n"
    msg += f"_Monitorando {len(GATILHOS)} gatilhos de alta relevância_\n\n"
    
    if destaques:
        msg += "\n".join(destaques) + "\n\n"
    
    if radar:
        msg += "👀 *No Visor (Outras Trends):*\n" + "\n".join(radar)
        
    return msg

def enviar():
    try:
        conteudo = buscar_noticias_quentes()
        bot.send_message(CHAT_ID, conteudo, parse_mode='Markdown', disable_web_page_preview=True)
        print("✅ Relatório de inteligência enviado.")
    except Exception as e:
        print(f"❌ Falha no envio: {e}")

if __name__ == "__main__":
    enviar()
