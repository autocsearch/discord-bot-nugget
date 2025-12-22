import discord
from discord import app_commands
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("secrets")
SERVER_ID = int(os.getenv("ServerId"))
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# -------------- Finnhub Fetch --------------

def fetch_finnhub_news():
    url = "https://finnhub.io/api/v1/news"
    params = {
        "category": "general",
        "token": FINNHUB_API_KEY
    }
    r = requests.get(url, params=params, timeout=10)
    return r.json()


# ---------------- Buttons ----------------

class NewsView(discord.ui.View):
    def __init__(self, article_url: str):
        super().__init__(timeout=180)

        self.add_item(
            discord.ui.Button(
                label="Visit",
                style=discord.ButtonStyle.link,
                url=article_url
            )
        )

    @discord.ui.button(label="Explain", style=discord.ButtonStyle.primary)
    async def explain(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "This article highlights a recent market-related event that may impact investor sentiment.",
            ephemeral=True
        )


# ---------------- Events ----------------

@bot.event
async def on_ready():
    guild = discord.Object(id=SERVER_ID)
    await bot.tree.sync(guild=guild)
    print(f"Logged in as {bot.user} (slash commands synced)")


# ---------------- Slash Command ----------------

@bot.tree.command(
    name="news",
    description="Get today’s market news",
    guild=discord.Object(id=SERVER_ID)
)
async def news(interaction: discord.Interaction):
    await interaction.response.defer()  # prevents timeout

    articles = fetch_finnhub_news()

    if not articles:
        await interaction.followup.send("No market news available.")
        return

    article = articles[0]

    embed = discord.Embed(
        title=article["headline"],  # H1
        description=article["summary"],
        url=article["url"],
        color=discord.Color.gold()
    )

    embed.set_thumbnail(
        url="https://cdn.pixabay.com/photo/2024/02/18/10/25/finance-8580916_1280.png"
    )

    embed.add_field(
        name="Market Insight",
        value="This news may influence short-term market sentiment.",
        inline=False
    )

    embed.set_author(
        name="Market News Bot",
        icon_url="https://cdn.pixabay.com/photo/2023/03/31/12/36/ai-7886646_1280.png"
    )

    embed.set_footer(
        text=f"Source: {article['source']}"
    )

    view = NewsView(article["url"])

    await interaction.followup.send(embed=embed, view=view)


bot.run(TOKEN)
