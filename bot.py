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

GATILHOS = ['TRUMP', 'MUSK', 'ELON', 'BLACKROCK', 'ETF', 'FED', 'BTC', 'SOL', 'PEPE', 'RWA', 'AI', 'WHALE', 'DOGE', 'XRP', 'CARDANO', 'ADA']

# --- BANCO DE IMAGENS (Links estáveis) ---
IMAGENS_ZUEIRA = [
    "https://media.tenor.com/images/1c0155b486e929f6498ba4b3b02ba547/tenor.gif",
    "https://i.pinimg.com/originals/7d/44/1f/7d441fa14580436d10c5383505c24949.gif",
    "https://media1.giphy.com/media/trN9df5NmUOqCx21jo/giphy.gif",
    "https://cdn.pixabay.com/photo/2018/01/18/07/31/bitcoin-3089728_1280.jpg",
    "https://cdn.pixabay.com/photo/2021/05/09/13/10/finance-6240949_1280.jpg"
]

# --- CÉREBRO DA JP (GERADOR DE INSIGHTS) ---
def gerar_insight(titulo):
    titulo = titulo.upper()
    
    # Dicionário de reações baseadas em palavras-chave
    if any(x in titulo for x in ['CAPITULATE', 'FEAR', 'PANIC', 'CRASH', 'DUMP']):
        return "📉 *Análise:* O mercado está com medo extremo. Historicamente, quando o varejo capitula, as baleias começam a acumular. Pode ser uma oportunidade de compra fracionada."
    
    elif any(x in titulo for x in ['ATH', 'HIGH', 'SURGE', 'SOAR', 'MOON', 'BREAKOUT']):
        return "🚀 *Análise:* Momento de euforia e rompimento de topo. Cuidado com FOMO, mas a tendência é de alta forte. Ajuste os stop-loss."
    
    elif any(x in titulo for x in ['COMPRESS', 'CONSOLIDATE', 'SIDEWAYS', 'STABLE']):
        return "⚠️ *Análise:* O preço está comprimindo. Isso geralmente antecede um movimento explosivo (para cima ou para baixo). Aguarde a confirmação do rompimento."
    
    elif any(x in titulo for x in ['WHALE', 'BUYING', 'ACCUMULATE', 'INFLOW']):
        return "🐳 *Análise:* Dinheiro inteligente (Smart Money) entrando. Se as baleias estão comprando, a probabilidade de alta no médio prazo aumenta."
    
    elif any(x in titulo for x in ['SEC', 'SUING', 'LAWSUIT', 'BAN', 'REGULATION']):
        return "⚖️ *Análise:* Ruído regulatório gera volatilidade e quedas rápidas (FUD). Geralmente são boas chances de compra após o pânico inicial."
    
    elif any(x in titulo for x in ['AI', 'GPT', 'NVIDIA', 'TECH']):
        return "🤖 *Análise:* Narrativa de IA está muito forte. Moedas desse setor tendem a performar acima da média do Bitcoin."

    else:
        return "👀 *Conclusão:* Notícia neutra ou de impacto indireto. Fique atento ao volume nas próximas horas para confirmar a direção."

def buscar_noticias():
    print("----- JP SAFADA 4.0 (ANALISTA) -----")
    
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
        return None, f"Chefinho, a internet caiu aqui: {e}"

    destaques = []
    
    if 'results' in data:
        for post in data['results'][:8]: 
            titulo_en = post.get('title', '')
            
            # --- CORREÇÃO DA FONTE ---
            # Tenta pegar dentro de 'source' > 'title', se não der, pega 'domain'
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
                    # Tradução
                    try:
                        titulo_pt = tradutor.translate(titulo_en)
                    except:
                        titulo_pt = titulo_en 
                    
                    # GERA O INSIGHT
                    insight = gerar_insight(titulo_en)

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
        return None, "Mercado lateral, chefinho. Nada pra operar agora."

    cabecalho = "Oi chefinho, JP SAFADA trazendo o ouro pra você operar 💅🏻💰\n\n"
    corpo = "\n\n➖➖➖➖➖➖➖➖➖➖\n\n".join(destaques)
    msg_final = cabecalho + corpo
    
    imagem = random.choice(IMAGENS_ZUEIRA)
    
    return imagem, msg_final

if __name__ == "__main__":
    try:
        imagem, texto = buscar_noticias()
        
        if imagem and texto and "Nada pra operar" not in texto:
            try:
                bot.send_photo(CHAT_ID, photo=imagem, caption=texto, parse_mode='Markdown')
                print("✅ Foto + Análise enviada!")
            except:
                bot.send_message(CHAT_ID, texto, parse_mode='Markdown')
                print("✅ Texto enviado (Fallback).")
        
        elif texto:
            bot.send_message(CHAT_ID, texto)
            
    except Exception as e:
        print(f"❌ Erro: {e}")
