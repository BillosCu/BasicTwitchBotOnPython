from twitchio.ext import commands, sounds, routines
import random

bot_name = ""


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token="", client_secret="", prefix="!", initial_channels=[""])

        self.music_queue = []
        self.player = sounds.AudioPlayer(callback=self.player_done)

    async def player_done(self, ctx):
        await ctx.send('¡Eso es todo!')

    @commands.command()
    async def play(self, ctx, *args):
        text = " ".join(args)
        track = await sounds.Sound.ytdl_search(text)
        if not self.player.is_playing:
            await ctx.send(f'Sonando: {track.title}')
        else:
            await ctx.send(f'Luego se pone {track.title}')
            self.music_queue.append(track)

        self.player.play(track)
        print(track)
        print(self.player.is_playing)
        


    @commands.command()
    async def pause(self, ctx):
        if self.player.is_playing:
            self.player.pause()
            await ctx.reply("Pausado.")
        else:
            await ctx.send("No está sonando nada.")


    @commands.command()
    async def stop(self, ctx):
        if self.player.is_playing:
            self.player.stop()
            await ctx.reply("Se paró toda la música.")
        else:
            await ctx.send("No hay nada en la lista")

    @commands.command()
    async def resume(self, ctx):
        if self.player.is_paused:
            self.player.resume()
            await ctx.reply("Se paró toda la música.")
            self.player.is_playing = True
            self.player.is_paused = False
    

    @commands.command()
    async def volume(self, ctx, *args):
        try:
            volumen = int(args[0])
            if volumen>=1 and volumen<=100:
                self.player.volume = volumen
                await ctx.send(f"Volumen establecido en {volumen}%")
            else:
                await ctx.send("Digite Valores de 1 a 100")
        except:
            await ctx.send("No es un número")
        






# Inicializo el Bot
bot = Bot()

@routines.routine(seconds=20, iterations=0)
async def hello(ctx):
    await ctx.channel.send("/announcepurple ¡Gracias por estar aquí!")
    print("/announcepurple ¡Gracias por estar aquí!")

@bot.event()
async def event_ready():
    print(f"{bot_name.capitalize()} está funcionando.")


@bot.event()
async def event_message(ctx):
    if ctx.echo: #Si es un mensaje del bot, no lo toma en cuenta.
        return
        

    await bot.handle_commands(ctx)

    saludos = ['Hola HeyGuys', '¿Cómo estás? KonCha', 'Bienvenido/a TehePelo', 'Buenísimas BabyRage', 'Hi! 4Head']
    if ctx.content[0:4].lower() == 'hola' or ctx.content[0:3].lower() == 'ola':
        hello.start(ctx)
        await ctx.channel.send(f"/me {random.choice(saludos)} @{ctx.author.name}")


    if ctx.content.lower() == 'buena noche':
        await ctx.channel.send(f"/me Buena noche.")






#rate: cuantas veces se puede usar ese comando.
#per: Tiempo de cooldown
#bucket: Canal o miembro al que se le aplica el cd
@commands.cooldown(rate=1, per=10, bucket=commands.Bucket.member)
@bot.command(name="test")
async def test(ctx, *args):
    text = " ".join(args)
    if text == "":
        await ctx.reply(f"Test pasado {(ctx.author.display_name).capitalize()} sin argumentos")
    else:
        await ctx.reply(f"Test pasado {(ctx.author.display_name).capitalize()} con los argumentos \"{text}\"")


@commands.cooldown(rate=1, per=10, bucket=commands.Bucket.member)
@bot.command(name="bola8", aliases=['b8'])
async def bola8(ctx, *args):
    text = " ".join(args)
    choices = ['Sí', 'No', 'Oiganlo', 'No lo sé, tú dime']
    await ctx.reply(f"/me P: {text}\nR: {random.choice(choices)}")






if __name__ == '__main__':
    bot.run()