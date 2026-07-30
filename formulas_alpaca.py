import pandas as pd
import os
from dotenv import load_dotenv
import requests
from alpaca.trading.client import TradingClient

from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.live import StockDataStream
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed

### 1. FORMULAS PARA CARGAR DATOS DE ENTORNO
def load_env_variables():
    """Fórmula para cargar datos de entorno
    """
    load_dotenv()  # Cargar variables de entorno desde el archivo .env
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    Mi_URL = os.getenv("ENDPOINT")

#Inicio de sesion de cliente de Alpaca
    client = TradingClient(api_key=API_KEY,
                       secret_key=SECRET_KEY, 
                       paper=True
                       )
    cuenta = client.get_account()
    return API_KEY, SECRET_KEY, Mi_URL, client, cuenta



###2. Formula para cargar nuevas velas
async def procesar_nueva_vela(bar):
    print("----------------------------------------")
    print(f" Simbolo: {bar.symbol}")
    print(f" Precio de Cierre: ${bar.close}")
    print(f" Volumen transaccionado: {bar.volume}")
    print(f" Timestamp: {bar.timestamp}")



