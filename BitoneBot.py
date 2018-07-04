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
            "invitedUsers": ["@user1", "@user2", "@user3"]
            }
        }

#DB overwrite switch
overwriteDB = False

info = """Dear bounty hunters, we are very happy to announce our new presale bounty program!\n\n
This _Bounty Program_ objective is promoting the sales of *Bitone's* network by bringing users to our [official Telegram group](https://t.me/Bitone_Network).\n\n
Presale will be held on Q8 2018. We also have a bounty program planned for the 1st INO in Q10 2018. Tokens will be delivered 3 months later, during Q2 2019.\n\n
The score and bounty sheet will be constantly available for check in the [BN Bounty Presale](https://t.me/BN_bounty_presale) Telegram group.\n\n
How to participate in the *Bounty Program:*\n
    • Join [BN Bounty Presale](https://t.me/BN_bounty_presale) chat to participate, ask questions and clear doubts. `Do not use the chat for spam or ads.`\n
    • The violation of the campaign rules will lead to total *user disqualification* and abandonment of any rewards received by that time. * No kind of cheating will be tolerated.*\n
    • The *terms and conditions* of the BOUNTY campaign can be changed at any time if needed.\n\n
We also have special rewards that will be discussed individually. We are looking for partners with a significant name/reputation in the crypto/blockchain ecosystem.\nWe are also looking for marketing professionals to help with our marketing strategies (e.g. Able to organize events, social networks/SEO experts, etc.).\n\nThis bounty category should also bring those users that could connect us with assessors, influential people in the the crypto/blockchain world or those that add value to *Bitone Network* with fantastic ideas, and also those who can contribute to the develpment and/or auditory code.\n
You can reach us to get more details at `info@bitone.network` using *"Bounty"* as the email subject."""

informacion = """Estimados cazarecompensas, ¡estamos muy felices de anunciar nuestro nuevo programa de recompensas preventa!\n\n
El objetivo de este _Bounty Program_ es promocionar la preventa de la red *Bitone* atrayendo a nuestro [canal oficial de Telegram](https://t.me/Bitone_Network) a nuevos participantes.\n\n
Preventa se llevará a cabo en Q8 2018. También tendremos un programa de recompensas para el 1st INO en Q10 2018. Los tokens se distribuirán a los 3 meses más tarde, en Q2 2019.\n\n
La hoja de recompensas y puntuaciones será mostrada constantemente en el grupo de Telegram de [BN Bounty Presale](https://t.me/BN_bounty_presale).\n\n
Cómo acceder al *Programa Bounty:*\n
    • Únase al chat de [BN Bounty Presale](https://t.me/BN_bounty_presale) para participar, consultar y exponer dudas. `No hablar de spam o publicidad.`\n
    • La violación de las reglas de la campaña conduce a la *descalificación del participante* al abandonar todas las apuestas o fichas recibidas anteriormente. * No toleramos ningún tipo de trampa.*\n
    • Los *términos y condiciones* de la campaña BOUNTY pueden cambiarse en caso de necesidad.\n\n
También tenemos recompensas especiales que se negociarán individualmente. Estamos buscando socios con una huella/reconocimiento significativo en el ecosistema crypto/blockchain.\nTambién estamos buscando profesionales en el campo del marketing que nos ayuden con nuestra estrategia de marketing (p. Ej. Capaces de organizar eventos, SEO/profesionales de las redes sociales, etc.).\n\nEsta categoría de recompensas también debería atraer a los participantes que nos conectan con asesores, personas influyentes en la esfera crypto/blockchain o que aportan valor con ideas fantásticas para ayudar a *Bitone Network* y también a los contribuyentes al desarrollo y/o al código auditivo.\n
Consúltenos más detalles enviándonos un correo electrónico a `info@bitone.network` y escriba el asunto del correo electrónico *"Bounty"*."""

rules = """\n\n*How to participate?*\n
The goal is bringing users to Bitone Network's' [official Telegram group](https://t.me/Bitone_Network).

To participate, you must join the [BN Bounty Presale](https://t.me/BN_bounty_presale) Telegram group and read the pinned message with the steps to follow.

For each 50 invited users the paticipant brings, he will be rewarded with 0.250 Bitone Node, equal to 100 dolars at presale price.

Up to 100 Bitone Node will be handed to the participants during the event, worth 40.000 dolars at presale price.

The participant that brings more users to the Telegram group will get an extra reward of:

    • `1` Extra Bitone Node: If he invited a minimum of *100* users.

    • `5` Extra Bitone Node: If he invited a minimum of *500* users.

    • `10` Extra Bitone Node: If he invited a minimum of *1000* users.

*RULES:*

• Invited users must be real people and have to be crypto currencies users.

• The same user can't be invited twice.

• Invited users must remain in *Bitone Network's'* [official Telegram group](https://t.me/Bitone_Network) all the time during the presale campaign. In case a user leaves the group, his invitation will be taken away from the account of the participant the invitation belongs to.

• The campaign starts on june the 24th at 00:00 UTC + 2 ending on august the 31st at 00:00 UTC +2. During this time period everyone can participate and register, any moment.

• Any doubt or comments can be placed on [BN Bounty Presale](https://t.me/BN_bounty_presale) Telegram chat, but never in *Bitone Network's* official group.
"""

reglas = """\n\n*¿Cómo participar?*\n
El objetivo es atraer nuevos usuarios al [grupo oficial de Telegram](https://t.me/Bitone_Network) de Bitone Network.

Para participar, debe unirse al grupo de telegram [BN Bounty Presale](https://t.me/BN_bounty_presale) y leer los pasos a seguir en el mensaje anclado en el chat.

Por cada 50 nuevos invitados que traiga el participante, se le recompensará con 0,250 Bitone Node, un equivalente a 100 dólares a precio de preventa.

Se repartirán un máximo de 100 bitone node durante todo el evento, un equivalente a 40.000 dólares a precio de preventa.

El participante que haya traído más invitados al grupo de Telegram, obtendrá una recompensa extra de:

    • `1` Bitone Node extra: Si invitó a un mínimo de *100* personas.

    • `5` Bitone Node extra: Si invitó a un mínimo de *500* personas.

    • `10` Bitone Node extra: Si invito a un mínimo de *1000* personas.

*REGLAS:*

• Los usuarios invitados deben ser personas reales y deben estar en contacto con el entorno de las criptomonedas.

• No se podrá invitar más de una vez a un mismo usuario.

• Los usuarios invitados deben permanecer durante todo el evento de preventa dentro del [canal oficial de Telegram](https://t.me/Bitone_Network) de *Bitone Network*. En caso de que los invitados abandonen el chat, se descontará la puntuación correspondiente al participante que lo invito.

• La campaña compensará a partir del día 24 de junio a las 00:00 UTC + 2 y terminará el día 31 de agosto a las 00:00 UTC +2. Durante ese periodo de tiempo podrá participar todo el mundo e inscribirse en cualquier momento.

• Cualquier duda o comentario se hablará por el chat de Telegram de [BN Bounty Presale](https://t.me/BN_bounty_presale), nunca en el chat oficial de Telegram de *Bitone Network*.
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
            #mainAdmin = ["57208941", "407534480"]
            mainAdmin = ["57208941"]
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

def start(bot, update):
    chat_id = update.message.chat_id

    bot.send_message(chat_id=chat_id, text="Use /register command to start the register process.\n\nUsa el comando /registro para iniciar la subscripción al evento.", parse_mode="Markdown")


def register(bot, update):
    global users

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    msgId = update.message.message_id
    username = update.message.from_user.username
    registeredUsers = users.keys()
    chat = update.message.chat.type

    if chat != "private":
        msg = bot.send_message(chat_id=chat_id, text="Go to the bot @bitone\_network\_bot and start a conversation to begin the registration process.", parse_mode="Markdown")

        # Queue for deletion
        JQ.run_once(deleteMsg, 10, context=[chat_id, msg.message_id])
        JQ.run_once(deleteMsg, 10, context=[chat_id, msgId])

    else:
        if str(username) != "None":
            if username not in registeredUsers:
                users[str(username)] = {
                                        "chat_id": chat_id,
                                        "user_id": user_id,
                                        "enabled": False,
                                        "invitationCode": "",
                                        "invitedUsers": [],
                                        }

                bot.send_message(chat_id=user_id, text="Registration has been processed.")

                with open("Users.json", "w") as usersdb:
                        json.dump(users, usersdb)

                #avisarAdmins(bot, username)
                enableUser(bot, user_id, username)

            else:
                msg = bot.send_message(chat_id=user_id, text="You are registered already. It can only be done once.")

                # Queue for deletion
                JQ.run_once(deleteMsg, 10, context=[chat_id, update.message.message_id])

        else:
            bot.send_message(chat_id=user_id, text="A username is necessary to register. Set a username in your account settings then use the /register command again.")

        if chat != "private":
            # Queue for deletion
            JQ.run_once(deleteMsg, 10, context=[chat_id, update.message.message_id])


def registro(bot, update):
    global users

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    msgId = update.message.message_id
    username = update.message.from_user.username
    registeredUsers = users.keys()
    chat = update.message.chat.type

    if chat != "private":
        msg = bot.send_message(chat_id=chat_id, text="Ve con el bot @bitone\_network\_bot e inicia una conversación para empezar con el registro", parse_mode="Markdown")

        # Queue for deletion
        JQ.run_once(deleteMsg, 10, context=[chat_id, msg.message_id])
        JQ.run_once(deleteMsg, 10, context=[chat_id, msgId])

    else:
        if str(username) != "None":
            if username not in registeredUsers:
                users[str(username)] = {
                                        "chat_id": chat_id,
                                        "user_id": user_id,
                                        "enabled": False,
                                        "invitationCode": "",
                                        "invitedUsers": [],
                                        }

                bot.send_message(chat_id=user_id, text="Se ha hecho el registro.")

                with open("Users.json", "w") as usersdb:
                        json.dump(users, usersdb)

                #avisarAdmins(bot, username)
                habilitarUsuario(bot, user_id, username)

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

    for key in msgEnts:
        if key.type == "hashtag":
            if str(msgEnts[key]) == "#invitación":
                try:
                    inviteCode = update.message.text[12:22]
                    if str(username) != "None":
                        # Deletion queue
                        if userId in users.keys():
                            if userId != users[username]["user_id"]:
                                JQ.run_once(deleteMsg, 5, context=[chat_id, msgId])

                        guardarInvitacion(bot, chat_id, userId, username, inviteCode, msgId)
                    else:
                        msg = bot.send_message(chat_id=chat_id, text="No podemos procesar la invitación hasta que tu cuenta tenga un nombre de usuario. Puedes ponerte uno en la configuración de Telegram bajo el campo llamado 'username'.")

                        # Queue for deletion
                        JQ.run_once(deleteMsg, 10, context=[chat_id, msgId])
                        JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])
                except:
                    msg = bot.send_message(chat_id=chat_id, text="Hay un error en el formato del mensaje de invitación. Asegurate de haberlo escrito bien.")

                    # Queue for deletion
                    JQ.run_once(deleteMsg, 5, context=[chat_id, msg.message_id])

            elif str(msgEnts[key]) == "#invite":
                try:
                    inviteCode = update.message.text[8:18]
                    if str(username) != "None":
                        # Deletion queue
                        if userId in users.keys():
                            if userId != users[username]["user_id"]:
                                JQ.run_once(deleteMsg, 5, context=[chat_id, msgId])

                        storeInvite(bot, chat_id, userId, username, inviteCode, msgId)
                    else:
                        msg = bot.send_message(chat_id=chat_id, text="We can't process the invitation while your account has no username. You can assing one for yourself in Telegram settings.")

                        # Queue for deletion
                        JQ.run_once(deleteMsg, 10, context=[chat_id, msgId])
                        JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])
                except:
                    msg = bot.send_message(chat_id=chat_id, text="There's an error in the invite formatting. Make sure you typed it correctly.")

                    # Queue for deletion
                    JQ.run_once(deleteMsg, 5, context=[chat_id, msg.message_id])
            else:
                pass


def bienvenida(bot, update):
    global users
    global knownUsers
    global usersLookupTable

    chat_id = str(update.message.chat_id)

    for newMember in update.message.new_chat_members:
        if str(newMember.id) in knownUsers.keys():

            userId = newMember.id

            # Counting back returning users

            # Get the owner of the invite
            owner = knownUsers[str(userId)]

            # Add user to the owner count
            users[owner]["invitedUsers"].append(str(userId))

            # Update users profiles
            updateUsers()


def generarToken():
    clave = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return clave

def habilitarUsuario(bot, chat_id, username):
    global users
    global adminsIds

    registeredUsers = users.keys()

    # Checking privileges
    if username in registeredUsers:
        codigo = generarToken()
        users[username]["invitationCode"] = codigo
        users[username]["enabled"] = True
        bot.send_message(chat_id=users[username]["user_id"], text="Tu código de invitación es: " + codigo + ". \n \n El usuario que invites deberá usar el hashtag #invitación más este código al entrar al [grupo oficial de Bitone Network](https://t.me/Bitone_Network) para completar la invitación.\n\nEste código de invitación es solamente válido para el grupo oficial y *no debe usarse* en el grupo de Bounty.\n\n A continuación se te enviará un mensaje ya formateado que cómodamente puedes reenviar a tus invitados, y que a su vez ellos puedan reenviar o copiar/pegar en el grupo de *Bitone Network* a su ingreso.", parse_mode="Markdown")
        bot.send_message(chat_id=users[username]["user_id"], text="#invitación " + codigo)

        updateLookupTable()
        updateUsers()

    else:
        pass


def enableUser(bot, chat_id, username):
    global users
    global adminsIds

    registeredUsers = users.keys()

    # Checking privileges
    if username in registeredUsers:
        codigo = generarToken()
        users[username]["invitationCode"] = codigo
        users[username]["enabled"] = True
        bot.send_message(chat_id=users[username]["user_id"], text="Your invite code is: " + codigo + ". \n \nThe user you bring will have to use the hashtag #invite plus this code in Bitone Network's [official Telegram group](https://t.me/Bitone_Network) to count the invite as valid.\n\nThis invite code only works in the official group and *should not be used* in the Bounty group.\n\nWe will send you a message with the right formatting that you can forward to your guests, and they can later resend or copy/paste in *Bitone Network's* official group when they come in.")
        bot.send_message(chat_id=users[username]["user_id"], text="#invite " + codigo)

        updateLookupTable()
        updateUsers()

    else:
        pass


def avisarAdmins(bot, username):

    for i in adminsIds:
        bot.send_message(chat_id=i, text="Hay un nuevo registro para habilitar del usuario " + str(username) + ". Para validar la subscripción use el comando: /habilitar " + str(username))

def myId(bot, update):

    msg = bot.send_message(chat_id=update.message.chat_id, text="ID del chat: " + str(update.message.chat_id))

    JQ.run_once(deleteMsg, 10, context=[update.message.chat_id, msg.message_id])

def storeInvite(bot, chat_id, userId, username, inviteCode, msgId):
    global chatData
    global users
    global adminsIds
    global knownUsers

    updateKnownUsers()

    if str(chat_id) == "-1001340675042":
        msg = bot.send_message(chat_id=chat_id, text="El código de invitación debe usarse en el grupo oficial de [Bitone Network](https://t.me/Bitone_Network).\n\nThe invite code must be used in Bitone Network's [official Telegram group](https://t.me/Bitone_Network).", parse_mode="Markdown")

        # Queue for deletion
        JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])
    else:
        if str(inviteCode) not in usersLookupTable.keys():
            msg = bot.send_message(chat_id=chat_id, text="The code used does not belong to any invite key generated by Bitone Network's system.\n\nTo avoid errors we suggest forwarding the invite message or copying and pasting it.", parse_mode="Markdown")

            # Queue for deletion
            JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])

        else:
            if users[usersLookupTable[str(inviteCode)]]["user_id"] != userId:
                if str(userId) in knownUsers.keys():
                    msg = bot.send_message(chat_id=chat_id, text="This user has already been registered with an invite in the system.")

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
                    msg = bot.send_message(chat_id=chat_id, text="The user " + str(username) + " has been added to the system with an invite from @" + owner + ".")

                    # Queue for deletion
                    JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])

                    updateKnownUsers()
            else:
                pass
    # Queue for deletion
    JQ.run_once(deleteMsg, 15, context=[chat_id, msgId])


def guardarInvitacion(bot, chat_id, userId, username, inviteCode):
    global chatData
    global users
    global adminsIds
    global knownUsers

    updateKnownUsers()

    if str(chat_id) == "-1001340675042":
        msg = bot.send_message(chat_id=chat_id, text="El código de invitación debe usarse en el grupo oficial de [Bitone Network](https://t.me/Bitone_Network).\n\nThe invite code must be used in Bitone Network's [official Telegram group](https://t.me/Bitone_Network).", parse_mode="Markdown")

        # Queue for deletion
        JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])
    else:
        if str(inviteCode) not in usersLookupTable.keys():
            msg = bot.send_message(chat_id=chat_id, text="El código ingresado no pertenece a ninguna invitación emitida por el sistema de Bitone Network.\n\nPara evitar errores al copiar el código sugerimos redirigir el mensaje de invitación, o copiar y pegar.")

            # Queue for deletion
            JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])

        else:
            if users[usersLookupTable[str(inviteCode)]]["user_id"] != userId:
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
            else:
                pass

    # Queue for deletion
    JQ.run_once(deleteMsg, 15, context=[chat_id, msgId])


def showUsers(bot, update):
    global users
    global adminsIds
    global knownUsers

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
        msg = bot.send_message(chat_id="-1001340675042", text="El usuario " + member.username + " se ha salido del grupo.\n\nSe descontará la invitación del perfil del usuario @" + owner + " según las reglas.")

        msg2 = bot.send_message(chat_id="-1001340675042", text="The user " + member.username + " left the group.\n\nAccording to the rules, the invitation will be taken away from @" + owner + "'s profile.")

        # Deleting invite from owner
        try:
            users[owner]["invitedUsers"].remove(str(memberId))
        except:
            pass

        # Updating users DB
        updateUsers()

        # job queue for deletion
        JQ.run_once(deleteMsg, 15, context=[chat_id, msg.message_id])
        JQ.run_once(deleteMsg, 15, context=[chat_id, msg2.message_id])

def mostrarInfo(bot, update):
    global informacion

    chat_id = update.message.chat_id
    message_id = update.message.message_id

    if str(chat_id) == "-1001340675042":
        msg = bot.send_message(chat_id=chat_id, text=informacion, parse_mode="Markdown")

        # Queue for deletion
        JQ.run_once(deleteMsg, 5, context=[chat_id, message_id])
        JQ.run_once(deleteMsg, 70, context=[chat_id, msg.message_id])

    else:
        pass


def showInfo(bot, update):
    global info

    chat_id = update.message.chat_id
    message_id = update.message.message_id

    if str(chat_id) == "-1001340675042":
        msg = bot.send_message(chat_id=chat_id, text=info, parse_mode="Markdown")

        # Queue for deletion
        JQ.run_once(deleteMsg, 5, context=[chat_id, message_id])
        JQ.run_once(deleteMsg, 70, context=[chat_id, msg.message_id])

    else:
        pass

def mostrarReglas(bot, update):
    global reglas

    chat_id = update.message.chat_id
    message_id = update.message.message_id

    if str(chat_id) == "-1001340675042":
        msg = bot.send_message(chat_id=chat_id, text=reglas, parse_mode="Markdown")

        # Queue for deletion
        JQ.run_once(deleteMsg, 5, context=[chat_id, message_id])
        JQ.run_once(deleteMsg, 60, context=[chat_id, msg.message_id])

    else:
        pass


def showRules(bot, update):
    global rules

    chat_id = update.message.chat_id
    message_id = update.message.message_id

    if str(chat_id) == "-1001340675042":
        msg = bot.send_message(chat_id=chat_id, text=rules, parse_mode="Markdown")

        # Queue for deletion
        JQ.run_once(deleteMsg, 5, context=[chat_id, message_id])
        JQ.run_once(deleteMsg, 60, context=[chat_id, msg.message_id])

    else:
        pass

def stats(bot, update):
    global users
    global adminsIds
    global knownUsers

    chat_id = update.message.chat_id
    msgId = update.message.message_id

    if str(chat_id) == "-1001340675042":
        # Message
        messageToSend = "\n    *EVENT STATE*"

        for i in users.keys():

            # Preparing the text

            if i != "dummy":
                userText = "\n\n*• User: *`" + i + "`.    *Invited: *`"+ str(len(users[i]["invitedUsers"])) + "` members."
                messageToSend = messageToSend + userText
            else:
                pass

        msg = bot.send_message(chat_id=chat_id, text=messageToSend, parse_mode="Markdown")

        # Queue for deletion
        JQ.run_once(deleteMsg, 10, context=[chat_id, msg.message_id])
        JQ.run_once(deleteMsg, 60, context=[chat_id, msgId])

    else:
        pass


def estado(bot, update):
    global users
    global adminsIds
    global knownUsers

    chat_id = update.message.chat_id
    msgId = update.message.message_id

    if str(chat_id) == "-1001340675042":
        # Message
        messageToSend = "\n    *ESTADO DEL EVENTO*"

        for i in users.keys():

            # Preparing the text

            if i != "dummy":
                userText = "\n\n*• Usuario: *`" + i + "`.    *Invitados: *`"+ str(len(users[i]["invitedUsers"])) + "` miembros."
                messageToSend = messageToSend + userText
            else:
                pass


        msg = bot.send_message(chat_id=chat_id, text=messageToSend, parse_mode="Markdown")

        # Queue for deletion
        JQ.run_once(deleteMsg, 10, context=[chat_id, msg.message_id])
        JQ.run_once(deleteMsg, 60, context=[chat_id, msgId])

    else:
        pass


def userStats(bot, update):
    global users
    global usersLookupTable

    chat_id = update.message.chat_id
    msgId = update.message.message_id
    username = update.message.from_user.username
    #userId = update.message.from_user.id
    registeredUsers = usersLookupTable.values()

    if str(chat_id) == "-1001340675042":
        if username not in registeredUsers:
            msg = bot.send_message(chat_id=chat_id, text="You are not participating in the Bounty program. Nothing to show.")

            # Queue for deletion
            JQ.run_once(deleteMsg, 10, context=[chat_id, msg.message_id])

        else:
            invitedUsersCount = len(users[username]["invitedUsers"])

            msg = bot.send_message(chat_id=chat_id, text="Hi " + username + ". \n\nUp to now you have " + str(invitedUsersCount) + " users invited to Bitone Network's group.")

            # Queue for deletion
            JQ.run_once(deleteMsg, 20, context=[chat_id, msg.message_id])
            JQ.run_once(deleteMsg, 40, context=[chat_id, msgId])
    else:
        pass


def estadoUsuario(bot, update):
    global users
    global usersLookupTable

    chat_id = update.message.chat_id
    msgId = update.message.message_id
    username = update.message.from_user.username
    #userId = update.message.from_user.id
    registeredUsers = users.keys()

    if str(chat_id) == "-1001340675042":
        if username not in registeredUsers:
            print(registeredUsers)
            msg = bot.send_message(chat_id=chat_id, text="No estás participando del programa Bounty. Nada que mostrar.")

            # Queue for deletion
            JQ.run_once(deleteMsg, 10, context=[chat_id, msg.message_id])

        else:
            invitedUsersCount = len(users[username]["invitedUsers"])

            msg = bot.send_message(chat_id=chat_id, text="Hola " + username + ". \n\nHasta el momento llevas registrados " + str(invitedUsersCount) + " usuarios invitados en el grupo de Bitone Network.")

            # Queue for deletion
            JQ.run_once(deleteMsg, 20, context=[chat_id, msg.message_id])
            JQ.run_once(deleteMsg, 40, context=[chat_id, msgId])
    else:
        pass


def fullMsg(bot, update):
    global info
    global rules

    chat_id = update.message.chat_id

    if str(chat_id) == "-1001340675042":
        bot.send_message(chat_id=chat_id, text=info + rules, parse_mode="Markdown")
    else:
        pass

def msgCompleto(bot, update):
    global info
    global rules

    chat_id = update.message.chat_id

    if str(chat_id) == "-1001340675042":
        bot.send_message(chat_id=chat_id, text=informacion + reglas, parse_mode="Markdown")
    else:
        pass

def ayuda(bot, update):
    chat_id = update.message.chat_id
    msgId = update.message.message_id
    text = """*Los comandos disponibles para este bot son:*

    `/ayuda` - Muestra este mensaje.

    `/registro` - Para iniciar el proceso de registro y participar.

    `/estado` - Para ver la cantidad de invitados (personal).

    `/evento` - Para ver la cantidad de invitados (global)

    `/reglas` - Para mostrar las reglas que rigen este evento.

    `/informacion` - Para mostrar el mensaje de introducción al evento.

    `/codigo` - Para reenviar tu código de invitación.\n"""

    if str(chat_id) == "-1001340675042":
        msg = bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

        # Deletion queue
        JQ.run_once(deleteMsg, 30, context=[chat_id, msg.message_id])
        JQ.run_once(deleteMsg, 10, context=[chat_id, msgId])
    else:
        pass


def helpMsg(bot, update):
    chat_id = update.message.chat_id
    msgId = update.message.message_id
    text = """*Available commands for this bot are:*

    `/help` - Shows this help.

    `/register` - To start registration process and participate.

    `/stats` - To check the amount of invited users (personal).

    `/event` - To check the amount of invited users (global)

    `/rules` - To show the rules for this event.

    `/info` - To show the briefing for this event.

    `/code` - To retrieve your invite code.\n"""

    if str(chat_id) == "-1001340675042":
        msg = bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

        # Deletion queue
        JQ.run_once(deleteMsg, 30, context=[chat_id, msg.message_id])
        JQ.run_once(deleteMsg, 10, context=[chat_id, msgId])
    else:
        pass


def codigo(bot, update):
    global users

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    msgId = update.message.message_id
    codigo = ""

    if username in users.keys():
        codigo = "#invitación " + users[username]["invitationCode"]

        if str(chat_id) == "-1001340675042":
            bot.send_message(chat_id=user_id, text="Este es tu código de invitación:", parse_mode="Markdown")
            bot.send_message(chat_id=user_id, text=codigo, parse_mode="Markdown")

            # Deletion queue
            JQ.run_once(deleteMsg, 10, context=[chat_id, msgId])
        else:
            pass
    else:
        pass

def code(bot, update):
    global users

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    msgId = update.message.message_id
    codigo = ""

    if username in users.keys():
        codigo = "#invite " + users[username]["invitationCode"]

        if str(chat_id) == "-1001340675042":
            bot.send_message(chat_id=user_id, text="This is your invite code:", parse_mode="Markdown")
            bot.send_message(chat_id=user_id, text=codigo, parse_mode="Markdown")

            # Deletion queue
            JQ.run_once(deleteMsg, 10, context=[chat_id, msgId])
        else:
            pass
    else:
        pass


#Passing handlers to the dispatcher
DIS.add_handler(CMD("start", start))

DIS.add_handler(CMD("register", register))
DIS.add_handler(CMD("registro", registro))

DIS.add_handler(CMD("aAdmin", addAdmin, pass_args=True))

#DIS.add_handler(CMD("id", myId))
DIS.add_handler(CMD("ayuda", ayuda))
DIS.add_handler(CMD("help", helpMsg))

DIS.add_handler(CMD("codigo", codigo))
DIS.add_handler(CMD("code", code))

DIS.add_handler(CMD("full-es", msgCompleto))
DIS.add_handler(CMD("full", fullMsg))

DIS.add_handler(CMD("rules", showRules))
DIS.add_handler(CMD("reglas", mostrarReglas))

DIS.add_handler(CMD("informacion", mostrarInfo))
DIS.add_handler(CMD("info", showInfo))

DIS.add_handler(CMD("show", showUsers))

DIS.add_handler(CMD("event", stats))
DIS.add_handler(CMD("evento", estado))

DIS.add_handler(CMD("estado", estadoUsuario))
DIS.add_handler(CMD("stats", userStats))

DIS.add_handler(MSG(Filters.status_update.new_chat_members, bienvenida))
DIS.add_handler(MSG(Filters.status_update.left_chat_member, memberLeft))
DIS.add_handler(MSG(Filters.all, parsing))

inicio()
UPD.start_polling()