import os
import requests
import telebot
import random
from datetime import datetime, timedelta
from dateutil import parser
from deep_translator import GoogleTranslator

# --- CONFIGURAÇÕES ---
TOKEN_TELEGRAM = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
API_CRYPTOPANIC = os.environ.get('CRYPTOPANIC_KEY', '').strip()

bot = telebot.TeleBot(TOKEN_TELEGRAM)
tradutor = GoogleTranslator(source='auto', target='pt')

# --- MENSAGEM DE ERRO REAL ---
MSG_SEM_NOTICIAS = "Oi chefinho, JP SAFADA aqui 💅🏻\n\nVasculhei a última hora inteira e não achei NADA. O site deve estar sem atualizar ou caiu."

# --- GATILHOS (Apenas para dar destaque visual) ---
GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'BLACKROCK', 'ETF', 'FED', 'BTC', 'SOL', 'PEPE', 'RWA', 'AI', 'WHALE', 'DOGE', 'XRP', 'CARDANO', 'ADA', 'ETH', 'BINANCE', 'CRYPTO', 'SEC', 'USDT', 'TETHER']

# --- IMAGENS ---
IMAGENS_TRABALHO = [
    "https://images.unsplash.com/photo-1611974765270-ca1258634369?q=80&w=1000&auto=format&fit=crop", 
    "https://images.unsplash.com/photo-1642790106117-e829e14a795f?q=80&w=1000&auto=format&fit=crop", 
    "https://images.unsplash.com/photo-1621504450168-38f647311816?q=80&w=1000&auto=format&fit=crop", 
    "https://cdn.pixabay.com/photo/2017/09/07/08/54/money-2724241_1280.jpg", 
    "https://cdn.pixabay.com/photo/2021/04/30/16/47/binance-6219389_1280.jpg", 
    "https://images.unsplash.com/photo-1640340434855-6084b1f4901c?q=80&w=1000&auto=format&fit=crop"
]

# --- CÉREBRO H1 ---
def analise_rapida(titulo, par_moeda):
    titulo = titulo.upper()
    ativo = par_moeda if par_moeda else "o ativo"

    if any(x in titulo for x in ['HIT', 'REACH', 'BREAK', 'SURPASS', 'EXPLODE', 'TOP', 'LIQUIDATE']):
        return f"✅ *Alvo/Rompimento:* Movimento forte em {ativo}. Atenção a realização de lucros."
    elif any(x in titulo for x in ['CAPITULATE', 'FEAR', 'PANIC', 'CRASH', 'DUMP', 'DROP', 'LOW']):
        return f"📉 *Venda/Pânico:* Pressão vendedora em {ativo}. Busque repiques para Short."
    elif any(x in titulo for x in ['ATH', 'HIGH', 'SURGE', 'SOAR', 'MOON', 'BULL', 'UP']):
        return f"🚀 *Alta:* Tendência forte de compra em {ativo}."
    else:
        return f"👀 *Radar:* Fique atento à volatilidade em {ativo}."

def buscar_noticias():
    print("----- JP SAFADA 10.0 (MODO ASPIRADOR) -----")
    
    url = "https://cryptopanic.com/api/developer/v2/posts/" 
    
    # PEGA TUDO (SEM FILTRO)
    params = {
        "auth_token": API_CRYPTOPANIC,
        "public": "true",
        "kind": "news" 
    }
    
    headers = { "User-Agent": "Mozilla/5.0" }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        data = response.json()
    except Exception as e:
        return None, f"Chefinho, erro de conexão: {e}"

    destaques = []
    gerais = []
    
    # --- JANELA DE 60 MINUTOS (SEGURANÇA MÁXIMA) ---
    agora = datetime.utcnow()
    limite_tempo = agora - timedelta(minutes=60)
    
    print(f"🕒 UTC Agora: {agora}")

    if 'results' in data:
        for post in data['results']: 
            
            # 1. VERIFICA DATA
            if 'published_at' in post:
                try:
                    data_noticia = parser.parse(post['published_at']).replace(tzinfo=None)
                    if data_noticia < limite_tempo:
                        continue # Pula notícia velha
                except:
                    continue
            
            titulo_en = post.get('title', '')
            
            # 2. IDENTIFICA MOEDA
            par_usdt = None
            if 'currencies' in post and post['currencies']:
                codigo = post['currencies'][0].get('code')
                if codigo: par_usdt = f"{codigo}/USDT"
            
            # 3. LINK
            if 'url' in post: link = post['url']
            elif 'slug' in post: link = f"https://cryptopanic.com/news/{post['slug']}"
            else: link = "https://cryptopanic.com"

            # 4. TRADUÇÃO
            try: titulo_pt = tradutor.translate(titulo_en)
            except: titulo_pt = titulo_en

            # 5. LÓGICA DE GATILHO vs GERAL (AQUI TAVA O ERRO)
            eh_destaque = False
            for gatilho in GATILHOS:
                if gatilho in titulo_en.upper():
                    # É DESTAQUE!
                    analise = analise_rapida(titulo_en, par_usdt)
                    texto = (
                        f"🔥 *{gatilho} DETECTADO*\n"
                        f"🇧🇷 {titulo_pt}\n"
                        f"{analise}\n"
                        f"🔗 [Ler]({link})"
                    )
                    destaques.append(texto)
                    eh_destaque = True
                    break 
            
            # SE NÃO FOI DESTAQUE, ENTRA COMO GERAL (CORREÇÃO)
            if not eh_destaque:
                texto_geral = (
                    f"📰 *Radar Geral*\n"
                    f"🇧🇷 {titulo_pt}\n"
                    f"🔗 [Ler]({link})"
                )
                gerais.append(texto_geral)

    # COMBINA TUDO (Prioriza destaques + até 5 gerais)
    conteudo_final = destaques + gerais[:5]

    print(f"📊 Aprovados: {len(conteudo_final)} (Destaques: {len(destaques)} | Gerais: {len(gerais)})")

    if not conteudo_final:
        return None, MSG_SEM_NOTICIAS

    cabecalho = "Oi chefinho, JP SAFADA na área! 💅🏻\n(Monitorando últimos 60min)\n\n"
    corpo = "\n\n➖➖➖➖➖\n\n".join(conteudo_final)
    msg_final = cabecalho + corpo
    
    imagem = random.choice(IMAGENS_TRABALHO)
    
    return imagem, msg_final

if __name__ == "__main__":
    try:
        imagem, texto = buscar_noticias()
        
        if texto:
            if imagem:
                try:
                    bot.send_photo(CHAT_ID, photo=imagem, caption=texto, parse_mode='Markdown')
                    print("✅ Relatório enviado com Sucesso!")
                except Exception as e:
                    print(f"Erro ao enviar foto: {e}")
                    # Se falhar a foto, manda texto
                    bot.send_message(CHAT_ID, texto, parse_mode='Markdown')
            else:
                bot.send_message(CHAT_ID, texto)
                print("✅ Aviso enviado.")
            
    except Exception as e:
        print(f"❌ Erro Crítico: {e}")
