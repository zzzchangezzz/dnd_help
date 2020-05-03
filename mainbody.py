import discord
import asyncio
import random
from flask import Flask
from data import db_session
from data.classes import Classes
from data.spells import Magic
from flask import render_template
from discord.ext import commands

with open('info_texts/bottoken.txt', encoding="utf-8") as f:
    TOKEN = str(f.read())
LANG = "RU"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dnd_bot_works'
db_session.global_init("db/baza.sqlite")
session = db_session.create_session()
app.run(port=8080, host='127.0.0.1')


class HelperAsk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info')
    async def information(self, ctx, lang=None):
        global LANG
        if lang is None:
            lang = LANG
        else:
            lang = lang.upper()
        try:
            inf = ""
            if lang == "RU":
                with open('info_texts/russian.txt', encoding="utf-8") as f:
                    inf = f.read()
            elif lang == "EN":
                with open('info_texts/english.txt', encoding="utf-8") as f:
                    inf = f.read()
            else:
                if LANG == "RU":
                    inf = "Используйте '/info RU' или '/info EN' или '/info'" +\
                        " для данной команды"
                if LANG == "EN":
                    inf = "Use '/info RU' or '/info EN' or '/info'" +\
                        " for this command"
            await ctx.send(inf)
        except:
            pass

    @commands.command(name='switch')
    async def language(self, ctx):
        global LANG
        if LANG == "RU":
            LANG = "EN"
            await ctx.send("Now bot main language is english")
        elif LANG == "EN":
            LANG = "RU"
            await ctx.send("Теперь бот говорит по-русски")

    @commands.command(name='roll') # бросок кости
    async def rolling(self, ctx, dice):
        global LANG
        try:
            d = int("".join(dice.split("d")))
            if d <= 0:
                await ctx.send("Impossible")  # кость без граней
            else:
                roll = random.randint(1, d)
                if roll == 1:
                    if LANG == "RU":
                        message = "Выпало 1. Критическая неудача"
                    else:
                        message = "Rolled 1. Critical failure"
                elif roll == d:
                    if LANG == "RU":
                        message = "Выпало " + str(roll) + ". Критический успех"
                    else:
                        message = "Rolled " + str(roll) + ". Critical success"
                else:
                    if LANG == "RU":
                        message = "Выпало " + str(roll)
                    else:
                        message = "Rolled " + str(roll)
                await ctx.send(message)
        except:
            pass

    @commands.command(name='contacts')  # связь
    async def contacted(self, ctx):
        try:
            with open('info_texts/dev_cont.txt', encoding="utf-8") as contact:
                inf = contact.read()
                await ctx.send(inf)
        except:
            pass
    
    @commands.command(name='credits')  # "особая благодарность"
    async def creditored(self, ctx):
        try:
            with open('info_texts/credits.txt', encoding="utf-8") as f:
                cred = f.read()
                await ctx.send(cred)
        except:
            pass
            
    @commands.command(name='remember')
    async def act_list(self, ctx, *arguments):
        pass  # временная заглушка


bot = commands.Bot(command_prefix='/')
bot.add_cog(HelperAsk(bot))
bot.run(TOKEN)
