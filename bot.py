sent_users = set()

@BotzHub.on(events.ChatAction)
async def _(event):
    if on_join is False:
        return

    if not event.is_group:
        return

    if event.action_message:
        return

    if not (event.user_joined or event.user_added):
        return

    user = await event.get_user()

    # Bot-এর নিজের event ignore
    me = await BotzHub.get_me()
    if user.id == me.id:
        return

    # একই user-এর জন্য একবারই
    if user.id in sent_users:
        return
    sent_users.add(user.id)

    chat = await event.get_chat()
    title = chat.title or "this chat"
    pp = await BotzHub.get_participants(chat)
    count = len(pp)

    mention = f"[{get_display_name(user)}](tg://user?id={user.id})"
    name = user.first_name
    last = user.last_name
    fullname = f"{name} {last}" if last else name
    username = f"@{user.username}" if user.username else mention

    joined = await get_user_join(user.id)

    if joined:
        msg = welcome_msg.format(
            mention=mention,
            title=title,
            fullname=fullname,
            username=username,
            name=name,
            last=last,
            channel=f"@{channel}",
            count=count,
        )

        butt = [
            [Button.url("Channel", f"https://t.me/{channel}")]
        ]

    else:
        msg = welcome_not_joined.format(
            mention=mention,
            title=title,
            fullname=fullname,
            username=username,
            name=name,
            last=last,
            channel=f"@{channel}",
            count=count,
        )

        butt = [
            [
                Button.url("Channel 1", "https://t.me/night_gang_official_bot"),
                Button.url("Channel 2", "https://t.me/night_support_group"),
                Button.url("Channel 3", "https://t.me/night_premium_chanel"),
            ],
            [
                Button.inline("UnMute Me", data=f"unmute_{user.id}")
            ]
        ]

        await BotzHub.edit_permissions(
            event.chat.id,
            user.id,
            send_messages=False
        )

    await event.reply(msg, buttons=butt)
