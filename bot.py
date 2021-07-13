import discord
import datetime
import os
from baza_danych import *
from discord.ext import commands


client = commands.Bot(command_prefix="..")
client.remove_command('help')


@client.event
async def on_ready():
    print(f'everything is ok {client.user}')


@client.command()
async def help(ctx):
    embed = discord.Embed(title="Komendy",
                          description="komendy tylko dla nauczycieli, wy nie musicie się nimi przejmować :p..."
                                      "...............          \elementy opcjonalne\ ", color=0x0088ff)
    embed.add_field(name="..leckja @osoba \czas\ \dzień\ ",
                    value="czas = 1(podajemy w godzinach) \ndzien = dzisiaj w formacie RRRR - MM - DD", inline=True)
    embed.add_field(name="..dodaj_studenta @osoba imie nazwisko numer_tel status",
                    value="status przyda się później jak będziecie zawieszać zajęcia czy coś", inline=True)
    embed.add_field(name="..moje_lekcje \miesiąc\ ", value="miesiąc = obecny miesiąc format MM", inline=True)
    embed.add_field(name="..moi_uczniowie", value="zwraca tabelę z osobami z którymi mieliśmy zajęcia", inline=True)
    embed.add_field(name="..zmien_lekcje @osoba id_lekcji data czas",
                    value="czas i data to są wartości które są zmieniane", inline=True)
    await ctx.author.send(embed=embed, delete_after=120)


@client.command()
@commands.has_role("tutor")
async def lekcja(ctx, member : discord.Member, dur=1.0, day=str(datetime.date.today())):
    add_lesson(str(ctx.author).split('#')[1],str(member).split('#')[1], dur, str(day))
    await ctx.author.send(f'{ctx.author} rozpoczołeś lekcje z {member} na czas {dur}')


@client.command()
@commands.has_role("tutor")
async def dodaj_ucznia(ctx, member : discord.Member, imie, nazwisko, numer_telefonu, status=''):
    add_student(imie, nazwisko, numer_telefonu, str(member), status)
    await ctx.author.send(f'{member}, {imie}, {nazwisko}, {numer_telefonu} zostal dodany :D', delete_after=60)


@client.command()
@commands.has_role("tutor")
async def moje_lekcje(ctx, month=datetime.date.today().strftime("%m")):
    info = show_my_lesson(str(ctx.author).split('#')[1], month)
    embed = discord.Embed()
    for row in info:
        embed.add_field(name=f"{row[1]}", value=f'{row[0]}, {row[3]} {row[4]}, {row[2]}', inline=False)
    await ctx.author.send(embed=embed)


@client.command()
@commands.has_role("tutor")
async def moi_uczniowie(ctx):
    students = show_my_students(str(ctx.author).split('#')[1])
    embed = discord.Embed()
    for row in students:
        embed.add_field(name=f"{row[0]} {row[1]}", value=f'{row[2]} {row[3]}, {row[4]}', inline=False)
    await ctx.author.send(embed=embed)


@client.command()
@commands.has_role("tutor")
async def zmien_lekcje(ctx, member : discord.Member, lesson_id, date, time):
    change_lesson(str(ctx.author).split('#')[1],str(member).split('#')[1], lesson_id, date, time)
    await ctx.author.send(f'lekcja została zmieniona')


@client.command()
@commands.has_role("tutor")
async def zmien_dane_ucznia(ctx, member : discord.Member, imie, nazwisko, numer_tel, status):
    change_student(str(member), imie, nazwisko, numer_tel, status)
    await ctx.author.send(f"{member} dane zostały zmienione")

@client.command()
@commands.has_role("adminn")
async def dodaj_nauczyciela(ctx, member : discord.Member, imie, nazwisko):
    add_tutor(imie, nazwisko, str(member))
    await ctx.author.send(f'{member}, {imie}, {nazwisko} tutor zostal dodany :D', delete_after=60)


@client.command()
@commands.has_role("adminn")
async def lekcje(ctx, month=datetime.date.today().strftime("%m")):
    lessons = show_lessons(month)
    embed = discord.Embed()
    for row in lessons:
        embed.add_field(name=f"{row[1]}", value=f'{row[0]}, {row[3]} {row[4]}, {row[2]}', inline=False)
    await ctx.author.send(embed=embed)


@client.command()
@commands.has_role("adminn")
async def nauczyciele(ctx):
    nauczyciele = show_tutors()
    embed = discord.Embed()
    for row in nauczyciele:
        embed.add_field(name=f"{row[0]}", value=f'{row[1]}, {row[2]}', inline=False)
    await ctx.author.send(embed=embed)


@client.command()
@commands.has_role("adminn")
async def uczniowie(ctx):
    students = show_students()
    embed = discord.Embed()
    for row in students:
        embed.add_field(name=f"{row[0]} {row[1]}", value=f'{row[2]} {row[3]}, {row[4]}', inline=False)
    await ctx.author.send(embed=embed)


@client.command()
@commands.has_role("adminn")
async def policz_godziny(ctx, member : discord.Member, month=date.today().strftime("%m")):
        hours = count_hours(str(member).split('#')[1], month)
        godziny = sum([float(info[3]) for info in hours])

        embed = discord.Embed()
        embed.add_field(name=f"liczba przepracowanych godzin {member} w {month} miesiącu = {godziny}",
                        value="\n".join([str(info).replace('(', '').replace(')', '') for info in hours]))

        await ctx.author.send(embed=embed)

@client.command()
@commands.has_role("adminn")
async def zmien_dane_nauczyciela(ctx, member : discord.Member, imie, nazwisko):
    change_tutor(str(member), imie, nazwisko)
    await ctx.author.send(f"{member} dane zostały zmienione")



client.run(os.getenv('TOKEN'))
