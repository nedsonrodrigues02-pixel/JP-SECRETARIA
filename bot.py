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

# --- MENSAGEM QUANDO NÃO HÁ NOTÍCIAS ---
MSG_SEM_NOTICIAS = "Oi chefinho, JP SAFADA aqui 💅🏻\n\nO radar tá ligado, mas não caiu nada na rede nos últimos 45 min. Sigo monitorando! 👀"

# --- GATILHOS ---
GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'BLACKROCK', 'ETF', 'FED', 'BTC', 'SOL', 'PEPE', 'RWA', 'AI', 'WHALE', 'DOGE', 'XRP', 'CARDANO', 'ADA', 'ETH', 'BINANCE']

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
def analise_h1_confirmation(titulo, par_moeda):
    titulo = titulo.upper()
    ativo = par_moeda if par_moeda else "o ativo"

    if any(x in titulo for x in ['HIT', 'REACH', 'BREAK', 'SURPASS', 'EXPLODE', 'TOP', 'LIQUIDATE', 'JUMP']):
        return (
            f"✅ *ATUALIZAÇÃO: Confirmado!*\n"
            f"• Movimento esperado aconteceu (Rompimento/Alvo).\n"
            f"• *Ação:* Proteja o lucro ou cuidado com topo.\n"
            f"🎯 *Status:* Volatilidade alta em *{ativo}*."
        )

    elif any(x in titulo for x in ['CAPITULATE', 'FEAR', 'PANIC', 'CRASH', 'DUMP', 'LOW', 'DROP', 'SLIP']):
        return (
            f"📉 *Alerta de Short (Venda)*\n"
            f"• *H1:* Pressão vendedora. Rompimento de suporte.\n"
            f"• *Estratégia:* Venda em repiques (Pullback).\n"
            f"🎯 *Foco:* Médias curtas em *{ativo}*."
        )
    
    elif any(x in titulo for x in ['ATH', 'HIGH', 'SURGE', 'SOAR', 'MOON', 'BULL', 'RALLY']):
        return (
            f"🚀 *Alerta de Long (Compra)*\n"
            f"• *H1:* Tendência de alta clara.\n"
            f"• *Estratégia:* Compra no rompimento de máxima.\n"
            f"🎯 *Foco:* Stop no fundo anterior de *{ativo}*."
        )
    
    elif any(x in titulo for x in ['COMPRESS', 'CONSOLIDATE', 'SIDEWAYS', 'STABLE', 'SQUEEZE', 'RANGE']):
        return (
            f"⚠️ *Aguarde Confirmação*\n"
            f"• *H1:* Preço preso (Consolidação).\n"
            f"• *Alerta:* Marque topo/fundo e opere SÓ o rompimento.\n"
            f"🎯 *Foco:* Paciência em *{ativo}*."
        )
    
    else:
        return (
            f"👀 *Radar Ligado*\n"
            f"• *Análise:* Volume pode entrar a qualquer momento.\n"
            f"• *Dica:* Fique atento ao fechamento do candle de 1h.\n"
            f"🎯 *Ativo:* *{ativo}*."
        )

def buscar_noticias():
    print("----- JP SAFADA 9.0 (MODO DEBUG X9) -----")
    
    url = "https://cryptopanic.com/api/developer/v2/posts/" 
    
    # REMOVI O FILTER. PEGA TUDO.
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
    
    # --- NOVO TEMPO: 45 MINUTOS ---
    agora = datetime.utcnow()
    limite_tempo = agora - timedelta(minutes=45)
    
    print(f"🕒 Hora Agora (UTC): {agora}")
    print(f"🛑 Limite de Corte: {limite_tempo}")

    count_analisadas = 0
    
    if 'results' in data:
        for post in data['results']: 
            count_analisadas += 1
            
            titulo_log = post.get('title', 'Sem titulo')[:30]
            
            # CHECK DE DATA
            if 'published_at' in post:
                try:
                    data_noticia = parser.parse(post['published_at']).replace(tzinfo=None)
                    
                    # LOG X9: Mostra no GitHub o que ele tá vendo
                    # print(f"📰 Notícia: {titulo_log}... | Data: {data_noticia}")
                    
                    if data_noticia < limite_tempo:
                        # Se for velha, ignora
                        continue 
                except:
                    continue
            
            titulo_en = post.get('title', '')
            
            # DETECTOR DE MOEDA
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

            # LINK
            if 'url' in post:
                link = post['url']
            elif 'slug' in post:
                link = f"https://cryptopanic.com/news/{post['slug']}"
            else:
                link = "https://cryptopanic.com"

            # GATILHOS
            for gatilho in GATILHOS:
                if gatilho in titulo_en.upper():
                    try:
                        titulo_pt = tradutor.translate(titulo_en)
                    except:
                        titulo_pt = titulo_en 
                    
                    analise = analise_h1_confirmation(titulo_en, par_usdt)

                    texto_formatado = (
                        f"🔥 *{gatilho} DETECTADO (H1)*\n"
                        f"🇧🇷 *{titulo_pt}*\n\n" 
                        f"{analise}\n\n"
                        f"🔗 [Ler matéria completa]({link})"
                    )
                    destaques.append(texto_formatado)
                    print(f"✅ BINGO! Notícia aprovada: {titulo_en}")
                    break 
    
    print(f"📊 Total analisado: {count_analisadas} | Aprovados: {len(destaques)}")

    if not destaques:
        return None, MSG_SEM_NOTICIAS

    cabecalho = "Oi chefinho, JP SAFADA com atualizações de H1 pra você 💅🏻⏳\n\n"
    corpo = "\n\n➖➖➖➖➖➖➖➖➖➖\n\n".join(destaques)
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
                    print("✅ Relatório H1 enviado!")
                except:
                    bot.send_message(CHAT_ID, texto, parse_mode='Markdown')
            else:
                bot.send_message(CHAT_ID, texto)
                print("✅ Aviso de 'Sem Notícias' enviado.")
            
    except Exception as e:
        print(f"❌ Erro Crítico: {e}")
