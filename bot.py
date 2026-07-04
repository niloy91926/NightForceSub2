import logging
from telethon.utils import get_display_name
import re
from telethon import TelegramClient, events, Button
from decouple import config
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO
)

log = logging.getLogger("BotzHub")

log.info("Starting...")

try:
    bottoken = config("BOT_TOKEN")
    xchannel = config("CHANNEL")
    welcome_msg = config("WELCOME_MSG")
    welcome_not_joined = config("WELCOME_NOT_JOINED")
    on_join = config("ON_JOIN", cast=bool)
    on_new_msg = config("ON_NEW_MSG", cast=bool)
except Exception as e:
    log.error(e)
    exit()

BotzHub = TelegramClient("BotzHub", 6, "eb06d4abfb49dc3e3a1e0f581e").start(
    bot_token=bottoken
)

channels = [x.replace("@", "") for x in xchannel.split()]

async def get_user_join(user_id):
    for ch in channels:
        try:
            await BotzHub(GetParticipantRequest(channel=ch, participant=user_id))
        except UserNotParticipantError:
            return False
    return True


@BotzHub.on(events.ChatAction)
async def handler(event):
    if not on_join:
        return
    if not event.is_group:
        return

    if event.user_joined or event.user_added:
        user = await event.get_user()
        chat = await event.get_chat()

        title = chat.title or "this chat"
        count = len(await BotzHub.get_participants(chat))

        mention = f"[{get_display_name(user)}](tg://user?id={user.id})"
        name = user.first_name
        last = user.last_name
        fullname = f"{name} {last}" if last else name
        username = f"@{user.username}" if user.username else mention

        x = await get_user_join(user.id)

        if x:
            msg = welcome_msg.format(
                mention=mention,
                title=title,
                fullname=fullname,
                username=username,
                name=name,
                last=last,
                channel=f"@{channels[0]}",
                count=count,
            )
            butt = [[Button.url("Channel", f"https://t.me/{channels[0]}")]]

        else:
            msg = welcome_not_joined.format(
                mention=mention,
                title=title,
                fullname=fullname,
                username=username,
                name=name,
                last=last,
                channel=f"@{channels[0]}",
                count=count,
            )

            butt = [
                [
                    Button.url("Channel 1", "https://t.me/night_gang_official_bot"),
                    Button.url("Channel 2", "https://t.me/night_support_group"),
                    Button.url("Channel 3", "https://t.me/night_premium_chanel"),
                ],
                [Button.inline("UnMute Me", data=f"unmute_{user.id}")],
            ]

            await BotzHub.edit_permissions(
                event.chat.id,
                user.id,
                send_messages=False
            )

        await event.reply(msg, buttons=butt)


@BotzHub.on(events.NewMessage(incoming=True))
async def mute_msg(event):
    if event.is_private or not on_new_msg:
        return

    x = await get_user_join(event.sender_id)
    if x:
        return

    try:
        await BotzHub.edit_permissions(
            event.chat.id,
            event.sender_id,
            send_messages=False
        )
    except:
        return

    user = await event.get_sender()
    chat = await event.get_chat()

    mention = f"[{get_display_name(user)}](tg://user?id={user.id})"
    title = chat.title or "this chat"
    count = len(await BotzHub.get_participants(chat))

    msg = welcome_not_joined.format(
        mention=mention,
        title=title,
        fullname=user.first_name,
        username=f"@{user.username}" if user.username else mention,
        name=user.first_name,
        last=user.last_name,
        channel=f"@{channels[0]}",
        count=count,
    )

    butt = [
        [
            Button.url("Channel 1", "https://t.me/night_gang_official_bot"),
            Button.url("Channel 2", "https://t.me/night_support_group"),
            Button.url("Channel 3", "https://t.me/night_premium_chanel"),
        ],
        [Button.inline("UnMute Me", data=f"unmute_{event.sender_id}")],
    ]

    await event.reply(msg, buttons=butt)


@BotzHub.on(events.CallbackQuery(pattern=b"unmute_(.*)"))
async def unmute(event):
    uid = int(event.pattern_match.group(1).decode())

    if uid != event.sender_id:
        return

    x = await get_user_join(uid)

    if not x:
        await event.answer("Join channels first!", alert=True)
        return

    await BotzHub.edit_permissions(
        event.chat.id,
        uid,
        send_messages=True
    )

    await event.edit("Welcome! You are unmuted.")


@BotzHub.on(events.NewMessage(pattern="/start"))
async def start(event):
    buttons = [
        [
            Button.url("Channel 1", "https://t.me/night_gang_official_bot"),
            Button.url("Channel 2", "https://t.me/night_support_group"),
            Button.url("Channel 3", "https://t.me/night_premium_chanel"),
        ]
    ]

    await event.reply("Bot is running!", buttons=buttons)


log.info("Bot started...")
BotzHub.run_until_disconnected()
