# Imports
import logging
import credentials
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
import catalogo
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    CallbackQueryHandler,
    filters,
    ApplicationBuilder,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Variáveis globais
cat = None

# Funções
def atualiza_catalogo():
    global cat
    with open('catalogo.json', 'r', encoding='utf-8' ) as f:
        cat = catalogo.Root.from_dict(json.load(f))


# Keyboards
def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Serviços', callback_data='servicos')],
                [InlineKeyboardButton('Pacotes', callback_data='pacotes')],
                [InlineKeyboardButton('Assinaturas', callback_data='assinaturas')]]
    return InlineKeyboardMarkup(keyboard)

def servicos_keyboard():
    keyboard = []
    for index, servico in enumerate(cat.catalogo.servicos):
        keyboard.append([InlineKeyboardButton(servico.nome, callback_data="exibir_servico_" + str(index))])

    keyboard.append([InlineKeyboardButton('Voltar', callback_data='main')])

    return InlineKeyboardMarkup(keyboard)

def pacotes_keyboard():
    keyboard = []
    for index, pacote in enumerate(cat.catalogo.pacotes):
        keyboard.append([InlineKeyboardButton(pacote.nome, callback_data="exibir_pacote_" + str(index))])

    keyboard.append([InlineKeyboardButton('Voltar', callback_data='main')])

    return InlineKeyboardMarkup(keyboard)

def assinaturas_keyboard():
    keyboard = []
    for index, assinatura in enumerate(cat.catalogo.assinaturas):
        keyboard.append([InlineKeyboardButton(assinatura.nome, callback_data="exibir_assinatura_" + str(index))])

    keyboard.append([InlineKeyboardButton('Voltar', callback_data='main')])

    return InlineKeyboardMarkup(keyboard)

def exibir_servico_keyboard(index):
    keyboard = [[InlineKeyboardButton('Voltar', callback_data='servicos')],
                [InlineKeyboardButton('Comprar', callback_data='comprar_servico_' + str(index))]
                ]
    
    return InlineKeyboardMarkup(keyboard)

def exibir_pacote_keyboard(index):
    keyboard = [[InlineKeyboardButton('Voltar', callback_data='pacotes')],
                [InlineKeyboardButton('Comprar', callback_data='comprar_pacote_' + str(index))]
                ]
    return InlineKeyboardMarkup(keyboard)

def exibir_assinatura_keyboard(index):
    keyboard = [[InlineKeyboardButton('Voltar', callback_data='assinaturas')],
                [InlineKeyboardButton('Comprar', callback_data='comprar_assinatura_' + str(index))]
                ]
    return InlineKeyboardMarkup(keyboard)

# Callbacks
async def callback_exibir_servicos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(text="Serviços", reply_markup=servicos_keyboard())

async def callback_exibir_pacotes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(text="Pacotes", reply_markup=pacotes_keyboard())

async def callback_exibir_assinaturas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(text="Assinaturas", reply_markup=assinaturas_keyboard())

async def callback_comprar_servico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # Query data = exibir_servico_{index}
    servico = cat.catalogo.servicos[int(query.data.split('_')[2])]

    chat_id = update.callback_query.message.chat_id
    title = servico.nome
    description = servico.descricao
    payload = "Custom-Payload"
    currency = "BRL"
    price = servico.valor
    prices = [LabeledPrice("Test", int(price * 100))]

    await context.bot.send_invoice(
        chat_id, title, description, payload, credentials.STRIPE_API_KEY, currency, prices
    )

async def callback_comprar_pacote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # Query data = exibir_pacote_{index}
    pacote = cat.catalogo.pacotes[int(query.data.split('_')[2])]

    chat_id = update.message.chat_id
    title = pacote.nome
    description = pacote.descricao
    payload = "Custom-Payload"
    currency = "BRL"
    price = pacote.valor
    prices = [LabeledPrice("Test", price * 100)]

    await context.bot.send_invoice(
        chat_id, title, description, payload, credentials.STRIPE_API_KEY, currency, prices
    )

async def callback_comprar_assinatura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # Query data = exibir_assinatura_{index}
    assinatura = cat.catalogo.assinaturas[int(query.data.split('_')[2])]

    chat_id = update.message.chat_id
    title = assinatura.nome
    description = assinatura.descricao
    payload = "Custom-Payload"
    currency = "BRL"
    price = assinatura.valor
    prices = [LabeledPrice("Test", price * 100)]

    await context.bot.send_invoice(
        chat_id, title, description, payload, credentials.STRIPE_API_KEY, currency, prices
    )

async def callback_pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    if query.invoice_payload != "Custom-Payload":
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)


async def callback_successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="Compra efetuada com sucesso! Link do serviço: [Link aqui]")


# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Seja bem vindo ao [Insira nome aqui]", reply_markup=main_menu_keyboard())


async def exibir_info_servico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # Query data = exibir_servico_{index}
    index = int(query.data.split('_')[2])
    servico = cat.catalogo.servicos[index]

    await query.edit_message_text(text=f"{servico.nome}\n{servico.descricao}\n{servico.valor}\n\n{servico.imagem}", reply_markup=exibir_servico_keyboard(index))

async def exibir_info_pacote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # Query data = exibir_pacote_{index}
    index = int(query.data.split('_')[2])
    pacote = cat.catalogo.pacotes[index]

    await query.edit_message_text(text=f"{pacote.nome}\n{pacote.descricao}\n{pacote.valor}\n\n{pacote.imagem}", reply_markup=exibir_pacote_keyboard(index))

async def exibir_info_assinatura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # Query data = exibir_assinatura_{index}
    index = int(query.data.split('_')[2])
    assinatura = cat.catalogo.assinaturas[index]

    await query.edit_message_text(text=f"{assinatura.nome}\n{assinatura.descricao}\n{assinatura.valor}\n\n{assinatura.imagem}", reply_markup=exibir_assinatura_keyboard(index))

async def exibir_servicos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    atualiza_catalogo()

    final_message = "Esses são os serviços disponíveis:\n\n"

    for servico in cat.catalogo.servicos:
        final_message += f"{servico.nome} - {servico.descricao} - {servico.valor}\n"
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=final_message)


async def exibir_pacotes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    atualiza_catalogo()

    final_message = "Esses são os pacotes disponíveis:\n\n"

    for pacote in cat.catalogo.pacotes:
        final_message += f"{pacote.nome} - {pacote.descricao} - {pacote.valor}\n"
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=final_message)


async def exibir_assinaturas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    atualiza_catalogo()

    final_message = "Essas são as assinaturas disponíveis:\n\n"

    for assinatura in cat.catalogo.assinaturas:
        final_message += f"{assinatura.nome} - {assinatura.descricao} - {assinatura.valor}\n"
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=final_message)


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.edit_message_text(text="Escolha uma das opções abaixo:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Serviços", callback_data="servicos")],
            [InlineKeyboardButton("Pacotes", callback_data="pacotes")],
            [InlineKeyboardButton("Assinaturas", callback_data="assinaturas")]
        ]))
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Escolha uma das opções abaixo:", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Serviços", callback_data="servicos")],
            [InlineKeyboardButton("Pacotes", callback_data="pacotes")],
            [InlineKeyboardButton("Assinaturas", callback_data="assinaturas")]
        ]))

# Main
if __name__ == '__main__':
    atualiza_catalogo()

    application = ApplicationBuilder().token(credentials.API_KEY).build()

    handlers = []
    
    # Handlers de mensagens
    handlers.append(MessageHandler(filters.TEXT & (~filters.COMMAND), message))

    # Handlers de comandos
    handlers.append(CommandHandler('start', start))
    handlers.append(CommandHandler('servicos', exibir_servicos))
    handlers.append(CommandHandler('pacotes', exibir_pacotes))
    handlers.append(CommandHandler('assinaturas', exibir_assinaturas))

    # Handlers de callbacks
    handlers.append(CallbackQueryHandler(main_menu, pattern="main"))
    handlers.append(CallbackQueryHandler(callback_exibir_servicos, pattern="servicos"))
    handlers.append(CallbackQueryHandler(callback_exibir_pacotes, pattern="pacotes"))
    handlers.append(CallbackQueryHandler(callback_exibir_assinaturas, pattern="assinaturas")
                    )
    handlers.append(CallbackQueryHandler(exibir_info_servico, pattern="^exibir_servico"))
    handlers.append(CallbackQueryHandler(exibir_info_pacote, pattern="^exibir_pacote"))
    handlers.append(CallbackQueryHandler(exibir_info_assinatura, pattern="^exibir_assinatura_"))

    handlers.append(CallbackQueryHandler(callback_comprar_servico, pattern="^comprar_servico"))
    handlers.append(CallbackQueryHandler(callback_comprar_pacote, pattern="^comprar_pacote"))
    handlers.append(CallbackQueryHandler(callback_comprar_assinatura, pattern="^comprar_assinatura"))

    # Payment handlers
    handlers.append(PreCheckoutQueryHandler(callback_pre_checkout))

    # Success! Notify your user!
    handlers.append(MessageHandler(filters.SUCCESSFUL_PAYMENT, callback_successful_payment))
    

    for handler in handlers:
        application.add_handler(handler)
    
    application.run_polling()
   