import discord
import asyncio
import requests
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
API_key = "trnsl.1.1.20200504T185824Z.76b4157e101f4" \
          "9ef.04aa3ed94a537b2f4d449f3a5eabd9da5f3c10d2"
req_beg = "https://translate.yandex.net/api/v1.5/tr.json/translate?lang=ru-en&key=" +\
          API_key + "&text="

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
                    inf = "Используйте '/info RU' или '/info EN' или '/info'" \
                          " для данной команды"
                if LANG == "EN":
                    inf = "Use '/info RU' or '/info EN' or '/info'" \
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

    @commands.command(name='roll')  # бросок кости
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
            with open('info_texts/credits.txt', encoding="utf-8") as fl:
                cred = fl.read()
                await ctx.send(cred)
        except:
            pass
    
    @commands.command(name='potions')
    async def mixed_potions(self, ctx, result=None):
        global LANG
        mssg = ""
        if result is None or result < 1 or result > 100:
            result = random.randint(1, 100)
            mssg = "Результат броска: " + result + ". "
        if result == 1:
            mssg += "Смесь взрывается, причиняя экспериментатору урон силовым полем 6d10, а также урон" \
                    " силовым полем 1d10 всем существам в пределах 5 фт. от него."
        elif 1 < result <= 8:
            mssg += "Смесь становится поглощаемым ядом по выбору Мастера."
        elif 8 < result <= 15:
            mssg += "Оба зелья теряют свои свойства."
        elif 15 < result <= 25:
            mssg += "Одно из зелий теряет свои свойства."
        elif 25 < result <= 35:
            mssg += "Оба зелья продолжают работать, но их численные эффекты" \
                    " снижаются наполовину. Если в силу особенностей зелья эффект" \
                    " нельзя понизить, то зелье не работает."
        elif 35 < result <= 90:
            mssg += "Оба зелья работают нормально"
        elif 90 < result <= 99:
            mssg += "Численные эффекты и длительность действия одного из зелий удваиваются." \
                    " Если ни одно зелье не может быть модифицировано таким образом, то в этом" \
                    " случае они работают как обычно."
        elif result == 100:
            mssg += "Только одно зелье продолжает работать, но его эффект" \
                    " становится постоянным. Выберите наиболее простой эффект" \
                    " для того, чтобы сделать его постоянным, или же тот," \
                    " который кажется вам наиболее забавным. Например, зелье" \
                    " лечения может увеличить максимум хитов на 4, а масло" \
                    " эфирности может навсегда заточить персонажа на Эфирном" \
                    " Плане. На ваше усмотрение, назначьте заклинание, такое как" \
                    " рассеивание магии или снятие проклятья, которое может рассеять" \
                    " этот длительный эффект."
        if LANG == "EN":
            req = req_beg + mssg
            answer = requests.get(req).json()
            mssg = answer["text"][0]
        await ctx.send(mssg)

    @commands.command(name='class_list')
    async def classes_list(self, ctx):
        global session
        cl = ""
        for clas in session.query(Classes).all():
            cl += clas.title + "\n"
        await ctx.send(cl)
    
    @commands.command(name='magic_list')
    async def spells_list(self, ctx):
        global session
        mgc = ""
        for spl in session.query(Magic).all():
            mgc += spl.title + "\n"
        await ctx.send(mgc)

    @commands.command(name='magic_for')
    async def spells_list(self, ctx, cl_m):
        global session
        try:
            mgc = ""
            n = cl_m[1].upper() + cl_m[1:].lower()
            hreq = "%{}%".format(n)
            for m in session.query(Magic).filter(Magic.classes.like(hreq)).all():
                mgc += m.title + "\n"
        except:
            pass


bot = commands.Bot(command_prefix='/')
bot.add_cog(HelperAsk(bot))
bot.run(TOKEN)
