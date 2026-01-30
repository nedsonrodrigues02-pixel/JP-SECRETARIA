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

# --- GATILHOS (Mantenho os mesmos para pegar as notícias) ---
GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'BLACKROCK', 'ETF', 'FED', 'BTC', 'SOL', 'PEPE', 'RWA', 'AI', 'WHALE', 'DOGE', 'XRP', 'CARDANO', 'ADA', 'ETH', 'BINANCE']

# --- IMAGENS PROFISSIONAIS (TRADER/MERCADO FINANCEIRO) ---
IMAGENS_TRABALHO = [
    "https://images.unsplash.com/photo-1611974765270-ca1258634369?q=80&w=1000&auto=format&fit=crop", # Candlestick chart gold
    "https://images.unsplash.com/photo-1642790106117-e829e14a795f?q=80&w=1000&auto=format&fit=crop", # Bull market crypto
    "https://images.unsplash.com/photo-1621504450168-38f647311816?q=80&w=1000&auto=format&fit=crop", # Bitcoin digital
    "https://cdn.pixabay.com/photo/2017/09/07/08/54/money-2724241_1280.jpg", # Graph analysis
    "https://cdn.pixabay.com/photo/2021/04/30/16/47/binance-6219389_1280.jpg", # Coins generic
    "https://images.unsplash.com/photo-1640340434855-6084b1f4901c?q=80&w=1000&auto=format&fit=crop"  # Serious Crypto Blue
]

# --- CÉREBRO ANALÍTICO (Agora com indicação do PAR) ---
def gerar_insight(titulo, par_moeda):
    titulo = titulo.upper()
    
    # Se não achou moeda específica, usa termo genérico
    ativo = par_moeda if par_moeda else "o ativo mencionado"

    if any(x in titulo for x in ['CAPITULATE', 'FEAR', 'PANIC', 'CRASH', 'DUMP', 'LOW']):
        return f"📉 *Setup:* O mercado indica medo extremo. Baleias costumam acumular nessas zonas. Procure por divergências de alta no RSI para o par *{ativo}*."
    
    elif any(x in titulo for x in ['ATH', 'HIGH', 'SURGE', 'SOAR', 'MOON', 'BREAKOUT', 'BULL']):
        return f"🚀 *Setup:* Rompimento de topo detectado. A tendência é forte, mas cuidado com correções. Ajuste o Stop-Loss e siga a tendência de alta em *{ativo}*."
    
    elif any(x in titulo for x in ['COMPRESS', 'CONSOLIDATE', 'SIDEWAYS', 'STABLE', 'SQUEEZE']):
        return f"⚠️ *Setup:* Compressão de preço (Bandeira ou Triângulo). Aguarde o candle de força romper a consolidação para entrar a favor do movimento em *{ativo}*."
    
    elif any(x in titulo for x in ['WHALE', 'BUYING', 'ACCUMULATE', 'INFLOW', 'MOVE']):
        return f"🐳 *Setup:* Fluxo institucional detectado. Smart Money se posicionando. Acompanhe o volume financeiro no gráfico de 4H do *{ativo}*."
    
    elif any(x in titulo for x in ['SEC', 'SUING', 'LAWSUIT', 'BAN', 'REGULATION']):
        return f"⚖️ *Setup:* Notícia de impacto regulatório (FUD). Alta volatilidade esperada. Evite operar alavancado em *{ativo}* até o mercado digerir a notícia."

    else:
        return f"👀 *Conclusão:* Fique atento ao Price Action de *{ativo}*. Se perder o suporte imediato, aguarde repique para venda."

def buscar_noticias():
    print("----- JP SAFADA 5.0 (TRADER PRO) -----")
    
    url = "https://cryptopanic.com/api/developer/v2/posts/" 
    
    params = {
        "auth_token": API_CRYPTOPANIC,
        "public": "true",
        "filter": "hot",   # Apenas notícias quentes
        "kind": "news"
    }
    
    headers = { "User-Agent": "Mozilla/5.0" }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
    except Exception as e:
        return None, f"Chefinho, sem conexão com a exchange: {e}"

    destaques = []
    
    if 'results' in data:
        for post in data['results'][:8]: 
            titulo_en = post.get('title', '')
            
            # --- DETECTOR DE MOEDA (PARA O PAR USDT) ---
            par_usdt = None
            if 'currencies' in post and post['currencies']:
                # Pega a primeira moeda da lista (Ex: 'BTC')
                codigo = post['currencies'][0].get('code')
                if codigo:
                    par_usdt = f"{codigo}/USDT"
            
            # Se a API não der a moeda, tenta achar no título pelo gatilho
            if not par_usdt:
                for g in GATILHOS:
                    if g in titulo_en.upper() and len(g) <= 5: # Filtra tickers curtos
                        par_usdt = f"{g}/USDT"
                        break

            # --- CORREÇÃO DA FONTE ---
            fonte = "Desconhecida"
            if 'source' in post and 'title' in post['source']:
                fonte = post['source']['title']
            elif 'domain' in post:
                fonte = post['domain']

            # --- LINK ---
            if 'url' in post:
                link = post['url']
            elif 'slug' in post:
                link = f"https://cryptopanic.com/news/{post['slug']}"
            else:
                link = "https://cryptopanic.com"

            for gatilho in GATILHOS:
                if gatilho in titulo_en.upper():
                    try:
                        titulo_pt = tradutor.translate(titulo_en)
                    except:
                        titulo_pt = titulo_en 
                    
                    # GERA O INSIGHT COM O PAR ESPECÍFICO
                    insight = gerar_insight(titulo_en, par_usdt)

                    texto_formatado = (
                        f"🔥 *{gatilho} DETECTADO*\n"
                        f"🇧🇷 *{titulo_pt}*\n"
                        f"🗞️ _Fonte: {fonte}_\n\n"
                        f"{insight}\n\n"
                        f"🔗 [Ler matéria completa]({link})"
                    )
                    destaques.append(texto_formatado)
                    break 
    
    if not destaques:
        return None, "Mercado lateral, chefinho. Sem volatilidade para operar agora."

    # Mantive a intro da JP, mas agora o conteúdo é profissional
    cabecalho = "Oi chefinho, JP SAFADA trazendo setups e notícias 💅🏻📊\n\n"
    corpo = "\n\n➖➖➖➖➖➖➖➖➖➖\n\n".join(destaques)
    msg_final = cabecalho + corpo
    
    imagem = random.choice(IMAGENS_TRABALHO)
    
    return imagem, msg_final

if __name__ == "__main__":
    try:
        imagem, texto = buscar_noticias()
        
        if imagem and texto and "Mercado lateral" not in texto:
            try:
                bot.send_photo(CHAT_ID, photo=imagem, caption=texto, parse_mode='Markdown')
                print("✅ Relatório Trader enviado!")
            except:
                bot.send_message(CHAT_ID, texto, parse_mode='Markdown')
                print("✅ Texto enviado (Fallback).")
        
        elif texto:
            bot.send_message(CHAT_ID, texto)
            
    except Exception as e:
        print(f"❌ Erro: {e}")
