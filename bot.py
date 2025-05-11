import discord
from discord.ext import commands
from discord import app_commands
import os
import random
import aiofiles

TOKEN = os.getenv("TOKEN")
UPLOAD_FOLDER = 'files'

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.tree.command(name="add", description="Thêm file vào bộ nhớ bot")
async def add_file(interaction: discord.Interaction):
    if not interaction.attachments:
        await interaction.response.send_message("Bạn cần đính kèm 1 file!", ephemeral=True)
        return

    for attachment in interaction.attachments:
        file_path = os.path.join(UPLOAD_FOLDER, attachment.filename)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(await attachment.read())

    await interaction.response.send_message(f"Đã thêm {len(interaction.attachments)} file!", ephemeral=True)

@bot.tree.command(name="get", description="Lấy ngẫu nhiên một file từ bộ nhớ")
async def get_file(interaction: discord.Interaction):
    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        await interaction.response.send_message("Bộ nhớ không có file nào!", ephemeral=True)
        return

    file_name = random.choice(files)
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    await interaction.response.send_message(file=discord.File(file_path))
    os.remove(file_path)

@bot.tree.command(name="count", description="Xem số file còn lại trong bộ nhớ")
async def count_files(interaction: discord.Interaction):
    count = len(os.listdir(UPLOAD_FOLDER))
    await interaction.response.send_message(f"Số file còn lại: {count}", ephemeral=True)

@bot.tree.command(name="show", description="Hiển thị danh sách file trong bộ nhớ")
async def show_files(interaction: discord.Interaction):
    files = os.listdir(UPLOAD_FOLDER)
    if not files:
        await interaction.response.send_message("Không có file nào!", ephemeral=True)
        return
    file_list = "\n".join(files)
    await interaction.response.send_message(f"Các file trong bộ nhớ:\n```{file_list}```", ephemeral=True)

bot.run(TOKEN)
