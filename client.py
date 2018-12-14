import asyncio
import websockets
 
async def test():
 
    async with websockets.connect('ws://localhost:8880/ws') as websocket:
 
        #await websocket.send("{'method': 'withdrawal','date': '2018-12-14','account': 'bar','amt' : 8050,'ccy': 'EUR'}")
        await websocket.send("{'method': 'deposit','date': '2018-12-11','account': 'foo','amt' : 1000,'ccy': 'USD'}")
        #await websocket.send("{'method': 'transfer','date': '2018-10-09', 'to_account': 'foo','from_account': 'bar','amt': 1000,'ccy': 'USD' }")
        #await websocket.send("{'method': 'get_balances','date': '2018-10-09','account': 'kaka'}")
        try:
            response = await websocket.recv()
            print(response)
        except asyncio.streams.IncompleteReadError:
            pass
 
asyncio.get_event_loop().run_until_complete(test())