import pandas as pd
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.live import StockDataStream
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.enums import DataFeed

import formulas_alpaca as fa



# Importamos la funcion y cargamos los datos de entorno
API_KEY, SECRET_KEY, Mi_URL, client, cuenta = fa.load_env_variables()

# Iniciamos en StockHistorical
cliente_hist= StockHistoricalDataClient(api_key=API_KEY, secret_key=SECRET_KEY)


excel_file_path = "listado_seguimiento.xlsx"
print(f"-- Extrayendo símbolos de {excel_file_path}...")
Simbolos= pd.read_excel(excel_file_path, sheet_name="Hoja1")

print(f"-- Símbolos extraídos correctamente: {Simbolos["Simbolo"].tolist()}")

Simbolos.head(5)

print("-- Fijando parámetros de solicitud de datos")
request_params = StockBarsRequest(
    symbol_or_symbols=Simbolos["Simbolo"].tolist(),
    timeframe=TimeFrame(1, TimeFrameUnit.Minute),
    start=datetime(2026, 1, 1),
    feed=DataFeed.IEX
)

print("-- Solicitando datos históricos para la selección...")

barsets = cliente_hist.get_stock_bars(request_params)

df_historico = barsets.df
df_historico.reset_index(inplace=True)

col_format_float = ["open", "high", "low", "close"]
col_format_int = ["volume"]
col_format_str = ["symbol"]

df_historico[col_format_float] = df_historico[col_format_float].astype(float)
df_historico[col_format_int] = df_historico[col_format_int].astype(int)
df_historico[col_format_str] = df_historico[col_format_str].astype(str)

print(df_historico.head(5))

print(df_historico.info())


df_historico.to_excel("historico.xlsx", index=True)