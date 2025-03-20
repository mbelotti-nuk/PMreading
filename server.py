import asyncio
import random
import json
import pandas as pd
from datetime import datetime
from fastapi import FastAPI, WebSocket
import uvicorn
import serial

app = FastAPI()
host = "192.168.1.36" # "127.0.0.1"

data_storage = []


def read_pm_sensor(port='/dev/ttyUSB0'):
    ser = serial.Serial(port, 9600, timeout=1)  
    data = ser.read(10)  # 10 byte alla volta
    if len(data) == 10 and data[0] == 0xAA and data[9] == 0xAB:
        # il numero e' diviso in due: byte alto e byte basso
        # per ricostruire il numero devo spostare il byte alto di 8 cifre a sinistra
        # e poi sommarlo con il byte basso 
        # divido per 10 come da specifiche
        pm2_5 = ((data[3] << 8) + data[2]) / 10.0  
        pm10  = ((data[5] << 8) + data[4]) / 10.0  
        checksum = sum(data[2:8]) & 0xFF  
        
        if checksum == data[8]:  # Controllo se il checksum è corretto
            return pm2_5, pm10
            #print(f"PM2.5: {pm2_5} µg/m³, PM10: {pm10} µg/m³")
    return None, None


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        now = datetime.now()
        pm2_5, pm10 = read_pm_sensor()
        data_point = {
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "hour": now.strftime("%H"),
            "pm2_5": pm2_5,
            "pm10": pm10
        }
        if pm2_5 != None:
            data_storage.append(data_point)

        await websocket.send_text(json.dumps(data_point))
        await asyncio.sleep(1)  # Send data every minute

@app.get("/hourly_avg")
async def get_hourly_avg():
    df = pd.DataFrame(data_storage)
    if df.empty:
        return []

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    today = datetime.now().strftime("%Y-%m-%d")
    df_today = df[df["timestamp"].dt.strftime("%Y-%m-%d") == today]

    if df_today.empty:
        return []

    hourly_avg = df_today.groupby("hour")[["pm2_5", "pm10"]].mean().reset_index()
    return hourly_avg.to_dict(orient="records")

@app.get("/monthly_avg")
async def get_monthly_avg():
    df = pd.DataFrame(data_storage)
    if df.empty:
        return []

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["month"] = df["timestamp"].dt.strftime("%Y-%m")
    monthly_avg = df.groupby("month")[["pm2_5", "pm10"]].mean().reset_index()
    
    return monthly_avg.to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=8000)

