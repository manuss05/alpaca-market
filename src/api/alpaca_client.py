import os
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv, find_dotenv

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockLatestQuoteRequest
from alpaca.data.timeframe import TimeFrame

# Cargar variables de entorno desde el archivo .env
load_dotenv(find_dotenv())

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

if not API_KEY or not SECRET_KEY:
    raise ValueError("Credenciales de Alpaca no encontradas. Revisa tu archivo .env.")

# Inicializar cliente de datos de mercado
client = StockHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)


def get_latest_prices(symbols: list[str]) -> dict[str, float]:
    """
    Devuelve un diccionario con el precio ask/bid medio más reciente
    para una lista de tickers.
    """
    request_params = StockLatestQuoteRequest(symbol_or_symbols=symbols)
    quotes = client.get_stock_latest_quote(request_params)
    
    latest_prices = {}
    for symbol, quote in quotes.items():
        # Tomamos el punto medio entre ask y bid o el último ask/bid disponible
        if quote.ask_price and quote.bid_price:
            mid_price = (quote.ask_price + quote.bid_price) / 2
        else:
            mid_price = quote.ask_price or quote.bid_price or 0.0
        latest_prices[symbol] = round(mid_price, 2)
        
    return latest_prices


def get_historical_bars(symbols: list[str], days_back: int = 30) -> pd.DataFrame:
    """
    Descarga velas diarias históricas para los tickers solicitados
    y devuelve un DataFrame normalizado listo para graficar.
    """
    start_date = datetime.now() - timedelta(days=days_back)
    
    request_params = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame.Day,
        start=start_date
    )
    
    bars = client.get_stock_bars(request_params)
    
    # Convertir respuesta de Alpaca a DataFrame con MultiIndex (symbol, timestamp)
    df = bars.df
    
    # Reset de índice para facilitar manipulaciones posteriores en Pandas
    df = df.reset_index()
    
    # Normalizar timestamp a fecha simple
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.date
    
    return df[["symbol", "timestamp", "open", "high", "low", "close", "volume"]]