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
GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'BLACKROCK', 'ETF', 'FED', 'BTC', 'SOL', 'PEPE', 'RWA', 'AI', 'WHALE', 'DOGE', 'XRP', 'CARDANO', 'ADA', 'ETH', 'BINANCE']

# --- IMAGENS TRADER ---
IMAGENS_TRABALHO = [
    "https://images.unsplash.com/photo-1611974765270-ca1258634369?q=80&w=1000&auto=format&fit=crop", 
    "https://images.unsplash.com/photo-1642790106117-e829e14a795f?q=80&w=1000&auto=format&fit=crop", 
    "https://images.unsplash.com/photo-1621504450168-38f647311816?q=80&w=1000&auto=format&fit=crop", 
    "https://cdn.pixabay.com/photo/2017/09/07/08/54/money-2724241_1280.jpg", 
    "https://cdn.pixabay.com/photo/2021/04/30/16/47/binance-6219389_1280.jpg", 
    "https://images.unsplash.com/photo-1640340434855-6084b1f4901c?q=80&w=1000&auto=format&fit=crop"
]

# --- CÉREBRO AVANÇADO (FUTUROS & PRAZOS) ---
def analise_avancada(titulo, par_moeda):
    titulo = titulo.upper()
    ativo = par_moeda if par_moeda else "o ativo"

    # --- CENÁRIO 1: MEDO/QUEDA (DUMP) ---
    if any(x in titulo for x in ['CAPITULATE', 'FEAR', 'PANIC', 'CRASH', 'DUMP', 'LOW', 'DROP']):
        return (
            f"📉 *Estratégia Bearish (Queda)*\n"
            f"• *Curto Prazo (15m - 1h):* Alta pressão vendedora. Busque operações de **SHORT** em repiques de baixa.\n"
            f"• *Médio Prazo (Diário):* O RSI pode estar sobrevendido. Cuidado com shorts longos, baleias podem começar a defender essa região.\n"
            f"🎯 *Foco:* Scalping rápido na venda em *{ativo}*."
        )
    
    # --- CENÁRIO 2: EUFORIA/ALTA (PUMP) ---
    elif any(x in titulo for x in ['ATH', 'HIGH', 'SURGE', 'SOAR', 'MOON', 'BREAKOUT', 'BULL', 'JUMP']):
        return (
            f"🚀 *Estratégia Bullish (Alta)*\n"
            f"• *Curto Prazo (1h - 4h):* Momentum muito forte. **LONG** a favor da tendência é o ideal agora.\n"
            f"• *Longo Prazo (Semanal):* Ativo esticado. Se opera swing trade, aguarde um reteste (pullback) antes de entrar pesado, pois pode corrigir.\n"
            f"🎯 *Foco:* Surfar a alta com Stop curto em *{ativo}*."
        )
    
    # --- CENÁRIO 3: COMPRESSÃO/LATERAL (ACUMULAÇÃO) ---
    elif any(x in titulo for x in ['COMPRESS', 'CONSOLIDATE', 'SIDEWAYS', 'STABLE', 'SQUEEZE', 'RANGE']):
        return (
            f"⚠️ *Estratégia de Volatilidade*\n"
            f"• *Intraday (H1):* O preço está preso. Não opere no meio do gráfico. Aguarde rompimento.\n"
            f"• *Visão Macro:* Compressão precede explosão. Coloque alertas nas extremidades. Se romper pra cima, é **LONG** agressivo.\n"
            f"🎯 *Foco:* Paciência. O próximo movimento de *{ativo}* será violento."
        )
    
    # --- CENÁRIO 4: BALEIAS/INSTITUCIONAL (SMART MONEY) ---
    elif any(x in titulo for x in ['WHALE', 'BUYING', 'ACCUMULATE', 'INFLOW', 'MOVE', 'BLACKROCK']):
        return (
            f"🐳 *Rastreando as Baleias*\n"
            f"• *Curto Prazo:* Pode haver manipulação para estopar sardinhas (fake out). Cuidado com alavancagem alta.\n"
            f"• *Longo Prazo:* O Dinheiro Inteligente está entrando. A tendência primária de *{ativo}* se torna altista.\n"
            f"🎯 *Foco:* Comprar correções (Buy the Dip)."
        )

    # --- CENÁRIO 5: REGULAÇÃO/FUD (INCERTEZA) ---
    elif any(x in titulo for x in ['SEC', 'SUING', 'LAWSUIT', 'BAN', 'REGULATION']):
        return (
            f"⚖️ *Alerta de Risco (News Trading)*\n"
            f"• *Imediato:* O mercado odeia incerteza. Provável **DUMP** (queda) inicial por pânico.\n"
            f"• *Pós-Notícia:* Muitas vezes o mercado recupera em 'V'. Se operar Short, realize lucro rápido.\n"
            f"🎯 *Foco:* Proteja seu capital. Alta volatilidade em *{ativo}*."
        )

    else:
        # Genérico criativo
        return (
            f"👀 *Análise de Fluxo*\n"
            f"• *Curto Prazo:* Notícia neutra, siga o Price Action de 15 minutos.\n"
            f"• *Longo Prazo:* Sem impacto estrutural na tendência de *{ativo}* por enquanto.\n"
            f"🎯 *Foco:* Aguardar confirmação de volume."
        )

def buscar_noticias():
    print("----- JP SAFADA 6.0 (FUTUROS MASTER) -----")
    
    url = "https://cryptopanic.com/api/developer/v2/posts/" 
    
    params = {
        "auth_token": API_CRYPTOPANIC,
        "public": "true",
        "filter": "hot",
        "kind": "news"
    }
    
    headers = { "User-Agent": "Mozilla/5.0" }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
    except Exception as e:
        return None, f"Chefinho, a exchange travou aqui: {e}"

    destaques = []
    
    if 'results' in data:
        for post in data['results'][:8]: 
            titulo_en = post.get('title', '')
            
            # --- DETECTOR DE MOEDA ---
            par_usdt = None
            if 'currencies' in post and post['currencies']:
                codigo = post['currencies'][0].get('code')
                if codigo:
                    par_usdt = f"{codigo}/USDT"
            
            if not par_usdt:
                for g in GATILHOS:
                    if g in titulo_en.upper() and len(g) <= 5: 
                        par_usdt = f"{g}/USDT"
                        break

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
                    
                    # CHAMADA DA NOVA FUNÇÃO DE FUTUROS
                    analise = analise_avancada(titulo_en, par_usdt)

                    # --- MONTAGEM COMPLETA ---
                    texto_formatado = (
                        f"🔥 *{gatilho} DETECTADO*\n"
                        f"🇧🇷 *{titulo_pt}*\n\n" 
                        f"{analise}\n\n"
                        f"🔗 [Ler matéria completa]({link})"
                    )
                    destaques.append(texto_formatado)
                    break 
    
    if not destaques:
        return None, "Mercado lateral, chefinho. Sem setups de futuros agora."

    cabecalho = "Oi chefinho, JP SAFADA trazendo o Raio-X dos Futuros 💅🏻🕯️\n\n"
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
                print("✅ Relatório Futuros enviado!")
            except:
                bot.send_message(CHAT_ID, texto, parse_mode='Markdown')
                print("✅ Texto enviado (Fallback).")
        
        elif texto:
            bot.send_message(CHAT_ID, texto)
            
    except Exception as e:
        print(f"❌ Erro: {e}")
