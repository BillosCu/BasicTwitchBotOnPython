from twitchio.ext import commands, sounds, routines
import random

bot_name = "vioscobot"

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token="oauth:1xg24sgrj6mya0459asjd9rmcjmazr", client_secret="17h6hkd3odkvw4hfr1paftbdecv779", prefix="!", initial_channels=["viosco"])

        self.player = sounds.AudioPlayer(callback=self.player_done)

    async def player_done():
        print('Finished playing song!')

    @commands.command()
    async def play(self, ctx, *args):
        text = " ".join(args)
        track = await sounds.Sound.ytdl_search(text)
        self.player.play(track)
        print(track)
        if self.player.is_playing:
            await ctx.send(f'Sonando: {track.title}')
        else:
            await ctx.send(f'Luego se pone {track.title}')


    

# Inicializo el Bot ya que no me f
bot = Bot()

@routines.routine(seconds=20, iterations=0)
async def hello(ctx):
    await ctx.channel.send(f"/announcepurple ¡Gracias por estar aquí!")

@bot.event()
async def event_ready():
    print(f"{bot_name.capitalize()} está funcionando.")


@bot.event()
async def event_message(ctx):
    if ctx.echo:
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
    await ctx.reply(f"/me P: {text}\nQ: {random.choice(choices)}")









if __name__ == '__main__':
    bot.run()