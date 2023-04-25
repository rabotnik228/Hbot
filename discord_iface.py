import discord
from discord.ext import commands
from consts import *
from captch_part import captcha, syn_flood
from rst import main

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)


@bot.command(pass_context=True)
async def sf(ctx, ip, port, count):
    await ctx.send("Sending packages...")
    global stop
    stop = False
    try:
        syn_flood.main(ip, port, count)
    except PermissionError:
        stop = True
        await ctx.send("Пакеты не отправлены. Проверьте права пользователя")
    if not stop:
        await ctx.send("Пакеты отправлены")


@bot.command(pass_context=True)
async def rst(ctx, ip, port, count):
    await ctx.send("Starting sniff...")
    main(ip, port, count)
    await ctx.send("Finish sniff!")


@bot.command(pass_context=True)
async def reC(ctx, url):
    captcha.cor_capt(url)


@bot.command(pass_context=True)
async def bhs(ctx):
    await ctx.send(file=discord.File('/exes/brmd5.exe'))
    await ctx.send('Чтобы начать брутфорсить скачайте этот файл.')


@bot.command(pass_context=True)
async def h(ctx):
    for i in range(5):
        await ctx.send(comma[i - 1])


bot.run(settings['token'])
