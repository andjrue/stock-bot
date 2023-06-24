import yfinance as yf
import discord
from discord.ext import commands
from datetime import datetime, date, timedelta

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

### TO-DO ###
# 1.) Call the most recent stock price of a stock - COMPLETE
# 2.) Provide most recent news articles for a stock - REMOVED, did not work how I hoped it would
# 3.) Ability to set alerts for stock price moves
# 4.) If market is up 5% over 3 days play the show me the money gif - ADJUSTED, WIP (money command)
# 5.) Random picture of Gordon Gekko everytime someone says 'money'






# Init commands & prefix for bot
bot = commands.Bot(command_prefix = "!", intents=intents)


# Help Command - Will add more over time
@bot.command()
async def helpMe(ctx):
    await ctx.send('Here are a few commands you can use:\n !stockPick (TICKER) - When you use this command, input the ticker and it will show the most recent closing price.')


# Returns stock price for most recent day
@bot.command()
async def stockPick(ctx, ticker):
    if ticker is None:
        await ctx.send(f'{ctx.author.mention}, please enter the ticker of the stock price you\'d like to see')
        return

    stock = yf.Ticker(ticker)
    price_history = stock.history(period='1d')

    if price_history.empty:
        await ctx.send(f'No data available for the ticker: {ticker}')
        return


     # Format the date as mm/dd/yy
    price_history.index = price_history.index.strftime('%m/%d/%y')

    # Drop the 'Dividends' and 'Stock Splits' columns
    price_history = price_history[['Close', 'Volume']]

    await ctx.send(f'Stock: {ticker}\n\nToday\'s price:\n{price_history}')


# Can compare a stocks close to yesterdays - Need to make a few adjustments to this. Seems to be working ok. 
@bot.command()
async def money(ctx, input_ticker):
    
    ticker = yf.Ticker(input_ticker)
    ticker_symbol = ticker.info["symbol"]
    
    today = date.today()
    yesterday = today - timedelta(days=2)
    data = yf.download(ticker_symbol, start=yesterday, end=today)
    closing_price = data['Close']

    if len(closing_price) >= 2:
        if closing_price[-1] > closing_price[-2]:
            await ctx.send(f'{ticker_symbol} closed higher than yesterday')
            await ctx.send(f'Stock: {ticker_symbol}\n\nPrice\'s:\n{closing_price}')
        else:
            await ctx.send(f"Today's closing price of {ticker_symbol} is not higher than yesterday's closing price.")
            await ctx.send(f'Stock: {ticker_symbol}\n\nPrice\'s:\n{closing_price}')
    else:
        await ctx.send('Insufficient historical data available.')




    
    








# ******** TOKEN FOR BOT DO NOT DELETE **********
bot.run('##########')