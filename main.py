import discord
from discord.ext import commands
from discord import app_commands
import os
import asyncio
import time
from seleniumbase import Driver
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
USERNAME = os.getenv("login")
PASSWORD = os.getenv("pass")

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')
    try:
        bot.tree.clear_commands(guild=None)  
        bot.tree.add_command(reset)  
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.error
async def on_app_command_error(interaction, error):
    print(f"Erro no comando: {error}")
    await interaction.response.send_message(f"Ocorreu um erro: {error}", ephemeral=True)

@bot.tree.command(name="reset", description="Reset HWID", guild=discord.Object(id=1327681560387784788))
async def reset(interaction: discord.Interaction, usuario: str = "Faccin"):
    """Comando para reset"""
    await interaction.response.defer()  
    
    await asyncio.sleep(1)
    
    driver = Driver(uc=True)
    url = "https://keyauth.cc/login"
    driver.uc_open_with_reconnect(url, 2)
    driver.uc_gui_click_captcha()
    time.sleep(2)

    username_xpath = "/html/body/section/div/div[2]/div/form/div[3]/input"
    password_xpath = "/html/body/section/div/div[2]/div/form/div[4]/input"
    login_button_xpath = "/html/body/section/div/div[2]/div/form/button"
    users_button_xpath = "/html/body/div[1]/aside/div/div/div/div[3]/div[1]/ul/li/a"
    search_input_xpath = "/html/body/div[1]/div[2]/main/div/div/div/div/div/div[12]/div/div[1]/div[2]/div/label/input"
    table_rows_xpath = "/html/body/div[1]/div[2]/main/div/div/div/div/div/div[12]/div/div[2]/table/tbody/tr"
    resethwid_button_xpath = "/html/body/div[1]/div[2]/main/div/div/div/div/div/div[12]/div/div[2]/table/tbody/tr[1]/td[8]/form/div/ul/li[2]/button"

    try:
        driver.find_element("xpath", username_xpath).send_keys(USERNAME)
        driver.find_element("xpath", password_xpath).send_keys(PASSWORD)

        time.sleep(2)
        driver.find_element("xpath", login_button_xpath).click()

        time.sleep(2)
        driver.find_element("xpath", users_button_xpath).click()

        time.sleep(2)
        driver.find_element("xpath", search_input_xpath).send_keys(usuario)

        time.sleep(2)
        rows = driver.find_elements("xpath", table_rows_xpath)

        user_found = False
        for row in rows:
            name_xpath = ".//td[2]"
            actions_xpath = ".//td[8]/form/div/button"

            name_element = row.find_element("xpath", name_xpath)
            if name_element.text.strip() == usuario:
                actions_button = row.find_element("xpath", actions_xpath)
                actions_button.click()
                user_found = True
                break

        if not user_found:
            await interaction.followup.send(f"User `{usuario}` not found!")
            driver.quit()
            return

        time.sleep(2)
        driver.find_element("xpath", resethwid_button_xpath).click()

        await interaction.followup.send(f"HWID for user `{usuario}` has been successfully reset!")

    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}")
    finally:
        time.sleep(5)
        driver.quit()

bot.run(TOKEN)