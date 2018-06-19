#-*- coding: utf-8 -*-

from telegram.ext import Updater
from telegram.ext import CommandHandler as CMD
from telegram.ext import MessageHandler as MSG
from telegram.ext import Filters

from time import gmtime, strftime

import json
import logging
import string
import random
import pprint

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

#Bot token key pickup
TOKEN = ""
with open("bot.key", "r") as tokenFile:
    TOKEN = tokenFile.read()


UPD = Updater(token=TOKEN)
JQ = UPD.job_queue
DIS = UPD.dispatcher


#Dumped dictionary. Has another dict for each chat ID + a generic fallback one.
chatData = {}

adminsIds = []

knownUsers = {}

usersLookupTable = {}

users = {
    "dummy": {
            "chat_id": "chat_id",
            "user_id": "user_id",
            "enabled": False,
            "invitationCode": "CS6GDEV9",
            "invitedUsers": ["@user1", "@user2", "@user3"],
            }
        }

#DB overwrite switch
overwriteDB = False

info = """Estimados cazarecompensas, ¡estamos muy felices de anunciar nuestro nuevo programa de recompensas preventa!\n\n
El objetivo de este _Bounty Program_ es promocionar la preventa de la red *Bitone* atrayendo a nuestro canal oficial de Telegram a nuevos participantes.\n\n
Preventa se llevará a cabo en Q8 2018. También tendremos un programa de recompensas para el 1st INO en Q10 2018. Los tokens se distribuirán a los 3 meses más tarde, en Q2 2019.\n\n
La hoja de recompensas y puntuaciones será mostrada constantemente en el grupo de Telegram de [BN Bounty Presale](https://t.me/BN_bounty_presale).\n\n
Cómo acceder al *Programa Bounty:*\n
    • Únase al chat de [BN Bounty Presale](https://t.me/BN_bounty_presale) para participar, consultar y exponer dudas. `No hablar de spam o publicidad.`\n
    • La violación de las reglas de la campaña conduce a la *descalificación del participante* al abandonar todas las apuestas o fichas recibidas anteriormente. * No toleramos ningún tipo de trampa.*\n
    • Los *términos y condiciones* de la campaña BOUNTY pueden cambiarse en caso de necesidad.\n\n
También tenemos recompensas especiales que se negociarán individualmente. Estamos buscando socios con una huella/reconocimiento significativo en el ecosistema crypto/blockchain.\nTambién estamos buscando profesionales en el campo del marketing que nos ayuden con nuestra estrategia de marketing (p. Ej. Capaces de organizar eventos, SEO/profesionales de las redes sociales, etc.).\n\nEsta categoría de recompensas también debería atraer a los participantes que nos conectan con asesores, personas influyentes en la esfera crypto/blockchain o que aportan valor con ideas fantásticas para ayudar a [Bitone Network](http://www.bitone.network/) y también a los contribuyentes al desarrollo y/o al código auditivo.\n
Consúltenos más detalles enviándonos un correo electrónico a `info@bitone.network` y escriba el asunto del correo electrónico *"Bounty"*."""

rules = """*¿Cómo participar?*\n\n
El objetivo es atraer nuevos usuarios al grupo oficial de Telegram de Bitone Network.

Para participar, debe unirse al grupo de telegram [BN Bounty Presale](https://t.me/BN_bounty_presale) y leer los pasos a seguir en el mensaje anclado en el chat.

Por cada 50 nuevos invitados que traiga el participante, se le recompensará con 0,5 bitone node, un equivalente a 250 dólares a precio de preventa.

Se repartirán un máximo de 100 bitone node durante todo el evento, un equivalente a 40.000 dólares a precio de preventa.

El participante que haya traído más invitados al grupo de Telegram, obtendrá una recompensa extra de:

    • `1` bitone node extra: Si invitó a un mínimo de *100* personas.

    • `5` Bitone node extra: Si invitó a un mínimo de *500* personas.

    • `10` Bitone node: Si invito a un mínimo de *1000* personas.

*Reglas:*

• Los usuarios invitados deben ser personas reales y deben estar en contacto con el entorno de las criptomonedas.

• No se podrá invitar más de una vez a un mismo usuario.

• Los usuarios invitados deben permanecer durante todo el evento de preventa dentro del canal oficial de Telegram de *Bitone Network*. En caso de que los invitados abandonen el chat, se descontará la puntuación correspondiente al participante que lo invito.

• La campaña compensará a partir del día 24 de junio a las 00:00 UTC + 2 y terminará el día 31 de agosto a las 00:00 UTC +2. Durante ese periodo de tiempo podrá participar todo el mundo e inscribirse en cualquier momento.

• Cualquier duda o comentario se hablará por el chat de Telegram de [BN Bounty Presale](https://t.me/BN_bounty_presale), nunca en el chat oficial de Telegram de Bitone Network.
"""

def inicio():
    global chatData
    global users
    global adminsIds
    global knownUsers
    global usersLookupTable

    try:
        with open("Users.json", "r") as usersdb:
            users = json.load(usersdb)
        with open("Admins.json", "r") as adminsdb:
            adminsIds = json.load(adminsdb)
        with open("KnownUsers.json", "r") as knowndb:
            knownUsers = json.load(knowndb)
    except:
        pass

    # Making sure the control vars are not empty
    if len(adminsIds) < 1:
        with open("Admins.json", "w") as adminsdb:
            mainAdmin = ["57208941", "407534480"]
            json.dump(mainAdmin, adminsdb)

        with open("Admins.json", "r") as adminsdb:
            adminsIds = json.load(adminsdb)

    if len(knownUsers) < 1:
        with open("KnownUsers.json", "w") as knowndb:
            mainUser = {"dummy": "dummy"}
            json.dump(mainUser, knowndb)

        with open("KnownUsers.json", "r") as knowndb:
            knownUsers = json.load(knowndb)

    # Loading up dictionary lookup table
    updateLookupTable()

def updateLookupTable():
    global usersLookupTable

    # Emptying the dict to avoid old data
    usersLookupTable = {}

    for i in users.keys():
        userInvite = users[i]["invitationCode"]
        usersLookupTable[userInvite] = i


def updateUsers():
    global users
    global knownUsers

    with open("Users.json", "w") as usersdb:
                json.dump(users, usersdb)

    with open("KnownUsers.json", "r") as knowndb:
            knownUsers = json.load(knowndb)

def updateKnownUsers():
    global knownUsers

    with open("KnownUsers.json", "w") as knowndb:
        json.dump(knownUsers, knowndb)

    with open("KnownUsers.json", "r") as knowndb:
            knownUsers = json.load(knowndb)

# Getting user Chat ID
def start(bot, update):
    global users

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    registeredUsers = users.keys()
    chat = update.message.chat.type

    if str(username) != "None":
        if username not in registeredUsers:
            users[str(username)] = {
                                    "chat_id": chat_id,
                                    "user_id": user_id,
                                    "enabled": False,
                                    "invitationCode": "",
                                    "invitedUsers": [],
                                    }

            bot.send_message(chat_id=user_id, text="Se ha hecho el registro. Ahora debes esperar que un administrador lo apruebe.\n\nSe te informará cuando el proceso de inscripción haya terminado.")

            with open("Users.json", "w") as usersdb:
                    json.dump(users, usersdb)

            avisarAdmins(bot, username)

        else:
            msg = bot.send_message(chat_id=user_id, text="Ya te has registrado en el sistema. Solo puede hacerse una vez.")

            # Queue for deletion
            JQ.run_once(deleteMsg, 10, context=[chat_id, update.message.message_id])

    else:
        bot.send_message(chat_id=user_id, text="Para registrarse en el sistema es necesario tener un nombre de usuario. Puedes poner uno en las configuraciones de tu cuenta y luego usar el comando /registro en este bot nuevamente.")

    if chat != "private":
        # Queue for deletion
        JQ.run_once(deleteMsg, 10, context=[chat_id, update.message.message_id])


def addAdmin(bot, update, args):
    global adminsIds

    adminName = update.message.from_user.username
    adminID = update.message.from_user.id

    if adminName == "RREDesigns" or adminID in adminsIds:
        adminsIds.append(args[0])
        bot.send_message(chat_id=update.message.chat_id, text="Admin añadido a la DB.")

        with open("Admins.json", "w") as adminfile:
            json.dump(adminsIds, adminfile)

    else:
        bot.send_message(chat_id=update.message.chat_id, text="Solamente los usuarios autorizados pueden agregar administradores.")


def reset(bot, update):
    global overwriteDB
    chat_id = str(update.message.chat_id)
    admin = update.message.from_user.username

    if admin in chatData[str(chat_id)]["admins"]:
        overwriteDB = True
        bot.send_message(chat_id=chat_id, text="Ahora puede usar el setup.", disable_notification=True)
    else:
        bot.send_message(chat_id=chat_id, text="Solo usuarios habilitados pueden resetear los datos.", disable_notification=True)


def parsing(bot, update):
    global chatData
    global users
    global adminsIds
    global knownUsers

    msgEnts = update.message.parse_entities()
    chat_id = str(update.message.chat_id)
    userId = update.message.from_user.id
    username = update.message.from_user.username
    msgId = update.message.message_id


    #Hashtag parsing
    #if chat_id in chatData.keys(): For multisession chats.
    for key in msgEnts:
        if key.type == "hashtag":
            if str(msgEnts[key]) == "#invitación":
                try:
                    inviteCode = update.message.text[12:22]
                    if str(username) != "None":
                        storeInvite(bot, chat_id, userId, username, inviteCode)
                    else:
                        msg = bot.send_message(chat_id=chat_id, text="No podemos procesar la invitación hasta que tu cuenta tenga un nombre de usuario.\n\nPuedes ponerte uno en la configuración de Telegram bajo el campo llamado 'username'.")

                        # Queue for deletion
                        JQ.run_once(deleteMsg, 10, context=[chat_id, msgId])
                        JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])
                except:
                    msg = bot.send_message(chat_id=chat_id, text="Hay un error en el formato del mensaje de invitación. Asegurate de haberlo escrito bien.")

                    # Queue for deletion
                    JQ.run_once(deleteMsg, 5, context=[chat_id, msg.message_id])

                # Queue for deletion
                JQ.run_once(deleteMsg, 5, context=[chat_id, msgId])
            else:
                pass


def bienvenida(bot, update):

    chat_id = str(update.message.chat_id)

    for newMember in update.message.new_chat_members:
        saludo = chatData["generic"]["saludo"] + newMember.first_name + ". " + chatData["generic"]["bienvenida"]

        bot.send_message(chat_id=update.message.chat_id, text=saludo, disable_notification=True)


def bienvenidaTest(bot, update):
    chat_id = str(update.message.chat_id)

    #Checking if there's a stored session
    if chat_id in chatData.keys():
        saludo = chatData[str(chat_id)]["saludo"] + "@user. " + chatData[str(chat_id)]["bienvenida"]

        bot.send_message(chat_id=update.message.chat_id, text=saludo, disable_notification=True)

    else:
        pass


def cambiarTextoDeBienvenida(bot, update, args):
    chat_id = str(update.message.chat_id)

    #Checking if there's a stored session
    if chat_id in chatData.keys():
        if update.message.from_user.username in chatData[str(chat_id)]["admins"]:
            chatData[str(chat_id)]["bienvenida"] = " ".join(args)
            bot.send_message(chat_id=update.message.chat_id, text="Mensaje de bienvenida cambiado.", disable_notification=True)
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Solo los usuarios habilitados pueden cambiar el mensaje de bienvenida.", disable_notification=True)

    else:
        bot.send_message(chat_id=chat_id, text=("No hay una sesión guardada para este chat. Use el comando setup para comenzar a guardar perfiles de forma permanente.").decode("utf-8"))




def generarToken():
    clave = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return clave

def habilitarUsuario(bot, update, args):
    global users
    global adminsIds

    registeredUsers = users.keys()
    username = args[0]
    adminID = update.message.from_user.id
    chat_id = update.message.chat_id

    # Checking privileges
    if str(adminID) in str(adminsIds):
        if username in registeredUsers:
            codigo = generarToken()
            users[username]["invitationCode"] = codigo
            users[username]["enabled"] = True
            bot.send_message(chat_id=users[username]["user_id"], text="Tu código de invitación es: " + codigo + ". \n \n El usuario que invites deberá usar un hastag más este código al entrar al grupo para completar la invitación.\n\n A continuación se te enviará un mensaje que tú y tus invitados pueden reenviar.")
            bot.send_message(chat_id=users[username]["user_id"], text="#invitación " + codigo)

            bot.send_message(chat_id=adminID, text="Se envió el código de invitación al usuario")

            updateLookupTable()
            updateUsers()

        else:
            bot.send_message(chat_id=update.message.chat_id, text="El usuario no se encuentra registrado.")

    else:
        bot.send_message(chat_id=chat_id, text="Solo usuarios habilitados pueden habilitar registros.")


def avisarAdmins(bot, username):

    for i in adminsIds:
        bot.send_message(chat_id=i, text="Hay un nuevo registro para habilitar del usuario " + str(username) + ". Para validar la subscripción use el comando: /habilitar " + str(username))

def myId(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Tu ID de usuario es: " + str(update.message.from_user.id))

def storeInvite(bot, chat_id, userId, username, inviteCode):
    global chatData
    global users
    global adminsIds
    global knownUsers

    updateKnownUsers()

    if str(inviteCode) not in usersLookupTable.keys():
        msg = bot.send_message(chat_id=chat_id, text="El código ingresado no pertenece a ninguna invitación emitida por el sistema de Bitone Network.\n\nPara evitar errores al copiar el código sugerimos redirigir el mensaje de invitación, o copiar y pegar.")

        # Queue for deletion
        JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])

    else:
        if str(userId) in knownUsers.keys():
            msg = bot.send_message(chat_id=chat_id, text="Este usuario ya fue registrado como invitado en el sistema.")

            # Queue for deletion
            JQ.run_once(deleteMsg, 5, context=[chat_id, msg.message_id])
        else:
            # Get the owner of the invite
            owner = usersLookupTable[str(inviteCode)]

            # Add user to the owner count
            users[owner]["invitedUsers"].append(str(userId))

            # Update users profiles
            updateUsers()

            # Add new group memeber to known users list
            knownUsers[str(userId)] = usersLookupTable[str(inviteCode)]

            # Alert about new computed invite
            msg = bot.send_message(chat_id=chat_id, text="El usuario " + str(username) + " se ha agregado al sistema como invitado de @" + owner + ".")

            # Queue for deletion
            JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])

            updateKnownUsers()
            print(knownUsers)


def showUsers(bot, update):
    global chatData
    global users
    global adminsIds
    global knownUsers
    global stack

    chat_id = update.message.chat_id
    msgId = update.message.message_id
    storedUsers = users.keys()

    for i in storedUsers:
        msg = bot.send_message(chat_id=chat_id, text="Usuario:" + i + str(users[i]))
        JQ.run_once(deleteMsg, 5, context=[chat_id, msg.message_id])

    # Queue for deletion
    JQ.run_once(deleteMsg, 5, context=[chat_id, msgId])

def deleteMsg(bot,job):

    bot.delete_message(chat_id=job.context[0], message_id=job.context[1])

def memberLeft(bot, update):
    global users
    global adminsIds
    global knownUsers

    chat_id = update.message.chat_id
    member = update.message.left_chat_member
    memberId = member.id

    if str(memberId) in knownUsers.keys():
        owner = knownUsers[str(member.id)]
        msg = bot.send_message(chat_id=chat_id, text="El usuario " + member.username + " se ha salido del grupo.\n\nSe descontará la invitación del perfil del usuario @" + owner + " según las reglas.")

        # Deleting invite from owner
        users[owner]["invitedUsers"].remove(str(memberId))

        # Updating users DB
        updateUsers()

        # job queue for deletion
        JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])

def showInfo(bot, update):
    global info

    chat_id = update.message.chat_id
    message_id = update.message.message_id

    msg = bot.send_message(chat_id=chat_id, text=info, parse_mode="Markdown")

    # Queue for deletion
    JQ.run_once(deleteMsg, 5, context=[chat_id, message_id])
    JQ.run_once(deleteMsg, 40, context=[chat_id, msg.message_id])

def showRules(bot, update):
    global rules

    chat_id = update.message.chat_id
    message_id = update.message.message_id

    msg = bot.send_message(chat_id=chat_id, text=rules, parse_mode="Markdown")

    # Queue for deletion
    JQ.run_once(deleteMsg, 5, context=[chat_id, message_id])
    JQ.run_once(deleteMsg, 40, context=[chat_id, msg.message_id])


#Passing handlers to the dispatcher
DIS.add_handler(CMD("start", start))
DIS.add_handler(CMD("registro", start))
DIS.add_handler(CMD("aAdmin", addAdmin, pass_args=True))
DIS.add_handler(CMD("id", myId))
DIS.add_handler(CMD("reglas", showRules))
DIS.add_handler(CMD("info", showInfo))
DIS.add_handler(CMD("show", showUsers))
DIS.add_handler(CMD("bienvenida", cambiarTextoDeBienvenida, pass_args=True))
DIS.add_handler(CMD("bienvenidaTest", bienvenidaTest))
DIS.add_handler(CMD("habilitar", habilitarUsuario, pass_args=True))

DIS.add_handler(MSG(Filters.status_update.new_chat_members, bienvenida))
DIS.add_handler(MSG(Filters.status_update.left_chat_member, memberLeft))
DIS.add_handler(MSG(Filters.all, parsing))

inicio()
UPD.start_polling()