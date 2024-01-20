import discord
from discord.ext import commands
import asyncio
from twilio.rest import Client

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='', intents=intents)

# Konfigurasi Twilio
TWILIO_ACCOUNT_SID = 'AC06a909ee587f5e46fa5c6954cfc80528'
TWILIO_AUTH_TOKEN = '7bb4f003bf8163d376132b3820fb25d1'
TWILIO_PHONE_NUMBER = '+19012311573'
TWILIO_WEBHOOK_URL = 'http://your-webhook-url.com/twilio-webhook'

# Inisialisasi Klien Twilio
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Variabel untuk menyimpan 6 digit angka dari panggilan
six_digit_input = None

# Logika untuk menanggapi panggilan suara
@bot.command(name='call', help='Memulai panggilan suara dan meminta 6 digit angka')
async def initiate_call(ctx):
    global six_digit_input
    try:
        # Panggilan suara Twilio dengan TwiML untuk meminta 6 digit angka
        twiml_message = '<Response><Say>Terimakasih telah menggunakan layanan kami. Silakan ketikkan 6 digit angka kemudian tekan tanda pagar.</Say><Gather numDigits="6" action="/process-input" method="POST" /></Response>'
        twiml = twiml_message

        # Memulai panggilan dengan Twilio
        call = twilio_client.calls.create(
            to=ctx.author.voice.channel.members[0].voice.channel.name,
            from_=TWILIO_PHONE_NUMBER,
            twiml=twiml,
            status_callback=TWILIO_WEBHOOK_URL
        )

        # Menunggu pengguna memasukkan 6 digit angka
        while six_digit_input is None:
            await asyncio.sleep(1)

        # Kirim respons "Terimakasih" ke channel yang sama
        await ctx.send(f"Terimakasih! Anda telah memasukkan 6 digit angka: {six_digit_input}. Panggilan suara selesai.")

    except Exception as e:
        await ctx.send(f"Terjadi kesalahan saat memulai panggilan suara: {str(e)}")

# Logika untuk menanggapi pesan suara dengan 6 digit angka
@bot.event
async def on_message(message):
    global six_digit_input
    if message.author == bot.user:
        return

    # Periksa apakah pesan suara memuat 6 digit angka
    if message.content.isdigit() and len(message.content) == 6:
        six_digit_input = message.content

    await bot.process_commands(message)

# Logika untuk menanggapi perintah bot Discord lainnya
@bot.command(name='hello', help='Menampilkan pesan sapaan')
async def hello(ctx):
    await ctx.send('Halo!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Maaf, perintah tidak dikenali. Silakan coba lagi.")

@bot.command(name='ping', help='Menampilkan latency bot')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Ping bot: {latency} ms')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

bot.run('MTE5MDUwNTIyMjY1MzYyNDM2MQ.Gq0QqB.Hd6bMWZg91rlSqUp0JMb2ySfUjZdx21wGFKSMM')
