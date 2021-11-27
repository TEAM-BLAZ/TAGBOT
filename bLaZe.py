import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "**𝐇𝐄𝐋𝐋𝐎 👋**\n\n**ɪ'ᴍ ᴍᴇɴᴛɪᴏɴᴀʟʟ ʙᴏᴛ.....**\n**ɪ ᴄᴀɴ ᴍᴇɴᴛɪᴏɴ ᴀʟᴍᴏsᴛ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ 👻...**\n**\n**ᴄʟɪᴄᴋ /help ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ..",
    link_preview=False,
    buttons=(
      [
      [ Button.url('➕Aᴅᴅ Mᴇ Tᴏ Uʀ Gʀᴏᴜᴘ➕', 'https://t.me/Thbotbot?startgroup=true'),
      ],

      [
        Button.url('❣️ Cʜᴀᴛ Zᴏɴᴇ', 'https://t.me/THE_SHOWRUNNERS'),
        Button.url('📢 Uᴘᴅᴀᴛᴇꜱ Cʜᴀɴɴᴇʟ', 'https://t.me/THE_BLAZE_NETWORK')
      ]
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "𝐇𝐞𝐥𝐩 𝐌𝐞𝐧𝐮 𝐎𝐟 𝐌𝐞𝐧𝐭𝐢𝐨𝐧 𝐁𝐨𝐭\n\n🕹 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬:-  /utag\n\n𝐄𝐱𝐚𝐦𝐩𝐥𝐞: `/utag Hello..!`\n\n**ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀs ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇssᴀɢᴇ...**🤗"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
       [ Button.url('➕Aᴅᴅ Mᴇ Tᴏ Uʀ Gʀᴏᴜᴘ➕', 'https://t.me/Thbotbot?startgroup=true'),
      ],
      [
        Button.url('❣️ Cʜᴀᴛ Zᴏɴᴇ', 'https://t.me/THE_SHOWRUNNERS'),
        Button.url('📢 Uᴘᴅᴀᴛᴇꜱ Cʜᴀɴɴᴇʟ', 'https://t.me/THE_BLAZE_NETWORK')
      ]
     ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/utag ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.reply("**OO BHAI**🤨 **GROUP MAIN USE KRO ESE.. YHA NHI...**")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.reply("__Only admins can mention all!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.reply("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.reply("__I can't mention members for older messages! (messages which are sent before I'm added to group)__")
  else:
    return await event.reply("__Reply to a message or give me some text to mention others!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.reply('__There is no proccess on going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.reply('__Stopped.__')

print(">> BLAZE MENTIONBOT STARTED <<")
client.run_until_disconnected()

@Client.on_message(
    command(["^/tgu$", f"^/starthgh$"])
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""**☞ ✰Hᴇʟʟᴏ...{message.from_user.mention()} ❣**
**☞ ✰Iᴍ.. [}](https://t.me/})**
**☞ ✰Tʜɪs ɪs Vɪᴅᴇᴏ + Mᴜsɪᴄ🎶 RᴏBᴏᴛ .. **
**☞ 📢 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 :- [ᗷʟᴀᴢᴇ](https://t.me/THE_BLAZE_NETWORK) **
**☞ ✰Fᴏʀ Mᴏʀᴇ Hᴇʟᴘ Usᴇ Bᴜᴛᴛᴏɴs Bᴇʟᴏᴡ Aɴᴅ Aʙᴏᴜᴛ Aʟʟ Fᴇᴀᴛᴜʀᴇ Oғ Tʜɪs Bᴏᴛ, Jᴜsᴛ Tyᴘᴇ /help ** """,

