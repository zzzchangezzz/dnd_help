import discord
import asyncio
import requests
import random
from data import db_session
from data.classes import Classes
from data.spells import Magic
from data.races import Races
from data.connector import Connection
from discord.ext import commands

with open('info_texts/bottoken.txt', encoding="utf-8") as f:
    TOKEN = str(f.read())
LANG = "RU"
API_key = "trnsl.1.1.20200504T185824Z.76b4157e101f4" \
          "9ef.04aa3ed94a537b2f4d449f3a5eabd9da5f3c10d2"
req_beg = "https://translate.yandex.net/api/v1.5/tr.json/" \
          "translate?lang=ru-en&key=" + API_key + "&text="

db_session.global_init("db/baza.sqlite")
session = db_session.create_session()


class HelperAsk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info')  # помощь
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
                    inf = "Используйте '/info RU' или '/info EN' или " \
                          "'/info' для данной команды"
                if LANG == "EN":
                    inf = "Use '/info RU' or '/info EN' or '/info'" \
                          " for this command"
            await ctx.send(inf)
        except:
            pass

    @commands.command(name='switch')  # смена языка
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

    @commands.command(name='form')  # основные формулы
    async def formulas(self, ctx):
        global LANG
        try:
            pathway = 'info_texts/main_formulas.txt'
            if LANG == "EN":
                pathway = 'info_texts/main_formulas_en.txt'
            with open(pathway, encoding="utf-8") as fl:
                cred = fl.read()
                await ctx.send(cred)
        except:
            pass
    
    @commands.command(name='check')  # проверка характеристики
    async def checkmod(self, ctx, chrc=None):
        global LANG
        if chrc is None:
            if LANG == "EN":
                await ctx.send("command should be like /check <number>")
            else:
                await ctx.send("команда должна иметь вид /check <число>")
        else:
            if chrc.isdigit():
                a = int(chrc)
                modif = (a - 10) // 2
                if modif > 0:
                    modif = "+" + str(modif)
                else:
                    modif = str(modif)
                if LANG == "EN":
                    await ctx.send("Modifier is " + modif)
                else:
                    await ctx.send("Модификатор " + modif)
            else:
                if LANG == "EN":
                    await ctx.send("please enter the characteristic`s index")
                else:
                    await ctx.send("пожалуйста укажите характеристику числом")
    
    @commands.command(name='link')  # ссылки на сайт для рассчёта
    async def linked_in(self, ctx, *args):
        global LANG
        lt = "https://dungeon.su/loot/"
        s = "https://dungeon.su/scrolls/"
        b = "https://dungeon.su/encounter_difficulty/"
        kfm = list(args)
        message = ""
        if not kfm:
            if LANG == "EN":
                message = "command needs keys (b - battle difficulty," \
                          " s - scrolls generation, l - loot generation)"
            else:
                message = "команде нужны ключи (b - сложность боя," \
                          " s - генератор свитков, l - генератор добычи)"
        else:
            for i in kfm:
                if i == "l":
                    if LANG == "EN":
                        message += "Loot: " + lt + "\n"
                    else:
                        message += "Добыча:" + lt + "\n"
                if i == "s":
                    if LANG == "EN":
                        message += "Scrolls: " + s + "\n"
                    else:
                        message += "Свитки:" + s + "\n"
                if i == "b":
                    if LANG == "EN":
                        message += "Battle difficulty: " + b + "\n"
                    else:
                        message += "Сложность боя:" + b + "\n"
        await ctx.send(message)
    
    @commands.command(name='potions')  # результат смешения зелий
    async def mixed_potions(self, ctx, result=None):
        global LANG
        mssg = ""
        if result is None:
            result = random.randint(1, 100)
            mssg = "Результат броска: " + str(result) + ". "
        elif not result.isdigit() or int(result) > 100:
            result = random.randint(1, 100)
            mssg = "Некорректные данные. Результат броска: " + \
                   str(result) + ". "

        result = int(result)
        if result == 1:
            mssg += "Смесь взрывается, причиняя экспериментатору урон силовым" \
                    " полем 6d10, а также урон силовым полем 1d10 всем существам" \
                    " в пределах 5 фт. от него."
        elif 1 < result <= 8:
            mssg += "Смесь становится поглощаемым ядом по выбору Мастера."
        elif 8 < result <= 15:
            mssg += "Оба зелья теряют свои свойства."
        elif 15 < result <= 25:
            mssg += "Одно из зелий теряет свои свойства."
        elif 25 < result <= 35:
            mssg += "Оба зелья продолжают работать, но их численные эффекты" \
                    " снижаются наполовину. Если в силу особенностей зелья" \
                    " эффект нельзя понизить, то зелье не работает."
        elif 35 < result <= 90:
            mssg += "Оба зелья работают нормально"
        elif 90 < result <= 99:
            mssg += "Численные эффекты и длительность действия одного из " \
                    "зелий удваиваются. Если ни одно зелье не может быть" \
                    " модифицировано таким образом, то в этом случае они" \
                    " работают как обычно."
        elif result == 100:
            mssg += "Только одно зелье продолжает работать, но его эффект" \
                    " становится постоянным. Выберите наиболее простой эффект" \
                    " для того, чтобы сделать его постоянным, или же тот," \
                    " который кажется вам наиболее забавным. Например, зелье" \
                    " лечения может увеличить максимум хитов на 4, а масло" \
                    " эфирности может навсегда заточить персонажа на Эфирном" \
                    " Плане. На ваше усмотрение, назначьте заклинание, такое" \
                    " как рассеивание магии или снятие проклятья, которое" \
                    " может рассеять этот длительный эффект."
        if LANG == "EN":
            req = req_beg + mssg
            answer = requests.get(req).json()
            mssg = answer["text"][0]
            mssg += " \n Переведено сервисом «Яндекс.Переводчик» " \
                    "https://translate.yandex.ru/"
        await ctx.send(mssg)

    @commands.command(name='class_list')  # список классов
    async def classes_list(self, ctx):
        global session
        cl = ""
        for clas in session.query(Classes).all():
            cl += clas.title + "\n"
        await ctx.send(cl)

    @commands.command(name='magic_list')  # список заклинаний
    async def spells_list(self, ctx):
        global session
        mgc = ""
        for spl in session.query(Magic).all():
            mgc += spl.title + "\n"
        await ctx.send(mgc)

    @commands.command(name='magic_for')  # список заклинаний для данного класса
    async def spells_clss(self, ctx, cl_m=None):
        global session
        global LANG
        try:
            if cl_m is None:
                if LANG == "EN":
                    await ctx.send("Need parameter of class")
                else:
                    await ctx.send("Нужно указывать класс")
            else:
                # перевод на русский для соответствия бд
                asked = "https://translate.yandex.net/api/v1.5/tr." \
                        "json/translate?lang=en-ru&key=" + API_key + "&text=" + cl_m
                answer = requests.get(asked).json()
                cl_m = answer["text"][0]
                n = cl_m[0].upper() + cl_m[1:].lower()
                hreq = '%{}%'.format(n)
                cl_id = session.query(Classes).filter(Classes.title.like(hreq)).first()
                mssg = ""
                if cl_id is not None:
                    con = session.query(Connection).filter(Connection.class_id == cl_id.id).all()
                    for i in con:
                        mgcl = session.query(Magic).get(i.spell_id)
                        mssg += mgcl.title + "\n"
                else:
                    if LANG == "EN":
                        mssg += "Bot does not know spells for this class."
                    else:
                        mssg += "Бот не знает заклинаний для этого класса."
                await ctx.send(mssg)
        except:
            pass

    @commands.command(name='class')  # описание класса
    async def class_info(self, ctx, ttl=None):
        global session, LANG
        if ttl is None:
            if LANG == "EN":
                await ctx.send("command should be like: /class <name>")
            else:
                await ctx.send("шаблон команды: /class <название>")
        else:
            n = "%" + ttl + "%"
            brd = session.query(Classes).filter(Classes.title.like(n)).first()
            mssg = ""
            if brd is None:
                if LANG == "EN":
                    mssg += "Unfortunately, bot does not know this class. " \
                            "Check if you`ve written it correctly."
                else:
                    mssg += "К сожалению, бот не знает этот класс. Проверьте" \
                            " правильность написания."
            else:
                if LANG == "EN":
                    req = req_beg + str(brd.title)
                    answer = requests.get(req).json()
                    mssg = answer["text"][0] + "\n"
                    stppd = str(brd.content).split(".")
                    for i in stppd:
                        if i != "":
                            req = req_beg + i
                            answer = requests.get(req).json()
                            mssg += answer["text"][0]
                        mssg += "."
                    mssg += "\nПереведено сервисом «Яндекс.Переводчик»" \
                            " https://translate.yandex.ru/"
                else:
                    mssg += str(brd)
            await ctx.send(mssg)

    @commands.command(name='magic')  # описание заклинания
    async def spell_info(self, ctx, *name):
        global session, LANG
        if not name:
            if LANG == "EN":
                await ctx.send("command should be like: /magic <title>")
            else:
                await ctx.send("шаблон команды: /magic <название>")
        else:
            name = " ".join(list(name))
            n = "%" + name + "%"
            mc = session.query(Magic).filter(Magic.title.like(n)).first()
            mssg = ""
            if mc is None:
                if LANG == "EN":
                    mssg += "Unfortunately, bot does not know this spell. " \
                            "Check if you have written it correctly."
                else:
                    mssg += "К сожалению, бот не знает это заклинание." \
                            " Проверьте правильность написания."
            else:
                if LANG == "EN":
                    req = req_beg + str(mc.title)
                    answer = requests.get(req).json()
                    mssg = answer["text"][0] + "\n"
                    req = req_beg + str(mc.level)
                    answer = requests.get(req).json()
                    mssg += "Level: " + answer["text"][0] + "\n"
                    req = req_beg + str(mc.distance)
                    answer = requests.get(req).json()
                    mssg += "Distance: " + answer["text"][0] + "\n"
                    req = req_beg + str(mc.components)
                    answer = requests.get(req).json()
                    mssg += "Components: " + answer["text"][0] + "\n"
                    req = req_beg + str(mc.durability)
                    answer = requests.get(req).json()
                    mssg += "Durability: " + answer["text"][0] + "\n"
                    req = req_beg + str(mc.classes)
                    answer = requests.get(req).json()
                    mssg += "Classes: " + answer["text"][0] + "\n"
                    sed = str(mc.content).split(".")
                    for j in sed:
                        if j != "":
                            req = req_beg + j
                            answer = requests.get(req).json()
                            mssg += answer["text"][0]
                        mssg += "."
                    mssg += "\nПереведено сервисом «Яндекс.Переводчик»" \
                            " https://translate.yandex.ru/"

                else:
                    mssg = str(mc)
            await ctx.send(mssg)

    @commands.command(name='race_list')  # список рас
    async def races_list(self, ctx):
        global session
        rc = ""
        for race in session.query(Races).all():
            rc += race.name + "\n"
        await ctx.send(rc)

    @commands.command(name='race')  # описание расы
    async def race_info(self, ctx, nick=None):
        global session, LANG
        if nick is None:
            if LANG == "EN":
                await ctx.send("command should be like: /race <name>")
            else:
                await ctx.send("шаблон команды: /race <название>")
        else:
            n = "%" + nick + "%"
            r_inf = session.query(Races).filter(Races.name.like(n)).first()
            mssg = ""
            if r_inf is None:
                if LANG == "EN":
                    mssg += "Unfortunately, bot does not know this race. " \
                            "Check if you have written it correctly."
                else:
                    mssg += "К сожалению, бот не знает эту расу. Проверьте" \
                            " правильность написания."
            else:
                if LANG == "EN":
                    req = req_beg + str(r_inf.name)
                    answer = requests.get(req).json()
                    mssg = answer["text"][0] + "\n"
                    stppd = str(r_inf.description).split(".")
                    for i in stppd:
                        if i != "":
                            req = req_beg + i
                            answer = requests.get(req).json()
                            mssg += answer["text"][0]
                        mssg += "."
                    mssg += "\nПереведено сервисом «Яндекс.Переводчик»" \
                            " https://translate.yandex.ru/"
                else:
                    mssg += str(r_inf)
            await ctx.send(mssg)


bot = commands.Bot(command_prefix='/')
bot.add_cog(HelperAsk(bot))
bot.run(TOKEN)
