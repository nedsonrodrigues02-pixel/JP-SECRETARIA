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

# --- GATILHOS DE ATIVOS ---
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

# --- CÉREBRO DE CONFIRMAÇÃO E FUTUROS ---
def analise_h1_confirmation(titulo, par_moeda):
    titulo = titulo.upper()
    ativo = par_moeda if par_moeda else "o ativo"

    # 1. DETECTOR DE CONFIRMAÇÃO (ACONTECEU AGORA)
    # Palavras que indicam que o movimento JÁ ocorreu
    if any(x in titulo for x in ['HIT', 'REACH', 'BREAK', 'SURPASS', 'EXPLODE', 'TOP', 'LIQUIDATE', 'JUMP']):
        return (
            f"✅ *ATUALIZAÇÃO DE MERCADO: Confirmado!*\n"
            f"• O movimento esperado aconteceu. Notícia indica rompimento ou alvo atingido.\n"
            f"• *Ação:* Se já entrou, proteja o lucro (Stop Gain). Se não entrou, CUIDADO com comprar topo.\n"
            f"🎯 *Status:* Volatilidade alta confirmada em *{ativo}*."
        )

    # 2. DETECTOR DE QUEDA/MEDO (SETUP DE VENDA)
    elif any(x in titulo for x in ['CAPITULATE', 'FEAR', 'PANIC', 'CRASH', 'DUMP', 'LOW', 'DROP', 'SLIP']):
        return (
            f"📉 *Alerta de Short (Venda)*\n"
            f"• *H1:* Pressão vendedora forte. Rompimento de suporte detectado.\n"
            f"• *Estratégia:* Venda em repiques (Pullback de baixa).\n"
            f"🎯 *Foco:* Acompanhe médias móveis curtas em *{ativo}*."
        )
    
    # 3. DETECTOR DE ALTA/FORÇA (SETUP DE COMPRA)
    elif any(x in titulo for x in ['ATH', 'HIGH', 'SURGE', 'SOAR', 'MOON', 'BULL', 'RALLY']):
        return (
            f"🚀 *Alerta de Long (Compra)*\n"
            f"• *H1:* Tendência de alta clara. Entrada a favor do fluxo.\n"
            f"• *Estratégia:* Compra no rompimento do candle anterior de 1h.\n"
            f"🎯 *Foco:* Stop abaixo do último fundo de *{ativo}*."
        )
    
    # 4. DETECTOR DE LATERALIZAÇÃO (AGUARDAR)
    elif any(x in titulo for x in ['COMPRESS', 'CONSOLIDATE', 'SIDEWAYS', 'STABLE', 'SQUEEZE', 'RANGE']):
        return (
            f"⚠️ *Aguarde Confirmação*\n"
            f"• *H1:* O preço está preso (Consolidação). Não opere no meio do gráfico.\n"
            f"• *Alerta:* Marque o topo e o fundo da última hora. Opere APENAS o rompimento.\n"
            f"🎯 *Foco:* Paciência em *{ativo}*."
        )
    
    # 5. PADRÃO (INSTITUCIONAL/NEWS)
    else:
        return (
            f"👀 *Radar Ligado*\n"
            f"• *Análise:* Notícia relevante entrando. Pode gerar volume repentino.\n"
            f"• *Dica:* Fique atento ao fechamento do candle de 1h para confirmar a direção.\n"
            f"🎯 *Ativo:* *{ativo}*."
        )

def buscar_noticias():
    print("----- JP SAFADA 7.0 (H1 OPERATIONAL) -----")
    
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
        return None, f"Chefinho, deu falha na conexão: {e}"

    destaques = []
    
    # --- FILTRO DE TEMPO (35 MINUTOS) ---
    # Como o bot roda a cada 30 min, pegamos notícias dos últimos 35 min (5 min de margem)
    agora = datetime.utcnow()
    limite_tempo = agora - timedelta(minutes=35)

    if 'results' in data:
        for post in data['results']: # Removemos o limite [:8] para verificar todas recentes
            
            # Verificação de Data
            if 'published_at' in post:
                data_noticia = parser.parse(post['published_at']).replace(tzinfo=None)
                # SE A NOTÍCIA FOR VELHA, PULA ELA
                if data_noticia < limite_tempo:
                    continue
            
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
                    
                    # NOVA ANÁLISE COM CONFIRMAÇÃO
                    analise = analise_h1_confirmation(titulo_en, par_usdt)

                    texto_formatado = (
                        f"🔥 *{gatilho} DETECTADO (H1)*\n"
                        f"🇧🇷 *{titulo_pt}*\n\n" 
                        f"{analise}\n\n"
                        f"🔗 [Ler matéria completa]({link})"
                    )
                    destaques.append(texto_formatado)
                    break 
    
    if not destaques:
        # Se não tiver nada NOVO nos últimos 30 min, não manda nada (Silêncio é melhor que repetição)
        # Retorna None para ambos
        print("Nenhuma notícia nova nos últimos 35 minutos.")
        return None, None 

    cabecalho = "Oi chefinho, JP SAFADA com atualizações de H1 pra você 💅🏻⏳\n\n"
    corpo = "\n\n➖➖➖➖➖➖➖➖➖➖\n\n".join(destaques)
    msg_final = cabecalho + corpo
    
    imagem = random.choice(IMAGENS_TRABALHO)
    
    return imagem, msg_final

if __name__ == "__main__":
    try:
        imagem, texto = buscar_noticias()
        
        # Só envia se tiver texto (Se for None, ele ignora e não spamma)
        if texto:
            try:
                bot.send_photo(CHAT_ID, photo=imagem, caption=texto, parse_mode='Markdown')
                print("✅ Relatório H1 enviado!")
            except:
                bot.send_message(CHAT_ID, texto, parse_mode='Markdown')
                print("✅ Texto enviado (Fallback).")
        else:
            print("Bot rodou mas não houve novidades (Evitando spam).")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
