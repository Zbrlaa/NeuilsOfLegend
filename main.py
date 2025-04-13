from fastapi import FastAPI, HTTPException
from riot_api import get_account_by_name

app = FastAPI()

@app.get("/summoner/{gameName}/{tagLine}")
async def summoner(gameName: str, tagLine: str):
    if not gameName or not tagLine:
        raise HTTPException(status_code=422, detail="gameName and tagLine are required")
    
    try:
        data = await get_account_by_name(gameName,tagLine)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))