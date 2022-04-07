import os

import discord
from discord import SlashCommandOptionType
from dotenv import load_dotenv

from bot.models import Idea
from config import IDEA_CHANNEL, PARENT_GUILD

load_dotenv()

intents = discord.Intents.default()

bot_instance = discord.Bot(intents=intents)


@bot_instance.slash_command(name='provide', description='Подать идею на рассмотрение.', guild_ids=[PARENT_GUILD])
async def suggest_idea(
        ctx: discord.ApplicationContext,
        text: discord.Option(SlashCommandOptionType.string, required=True, description="Текст идеи"),
        attachment: discord.Option(SlashCommandOptionType.attachment, required=False,
                                   description="Картинка или файл (опционально)"
                                   ) = None
):
    ideas_channel = ctx.guild.get_channel(IDEA_CHANNEL)

    i = Idea.form_object(text=text, author=ctx.author, attachment=attachment, creation_date=discord.utils.utcnow())

    await i.send_idea(ideas_channel)

    await ctx.respond(embed=discord.Embed(title='Успешно!', colour=discord.Colour.green()), ephemeral=True)


@bot_instance.event
async def on_ready():
    print('Bot is running...')


bot_instance.run(os.getenv("TOKEN"))
