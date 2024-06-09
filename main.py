from fastapi import FastAPI, WebSocket, WebSocketDisconnect, WebSocketException
from starlette.websockets import WebSocketState
from parser.parser import VideoFinder
import logging
import asyncio

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now();
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);

            ws.onopen = function() {
                console.log("WebSocket connection established");
            };

            ws.onmessage = function(event) {
                var messages = document.getElementById('messages');
                var message = document.createElement('li');
                var content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            };

            ws.onclose = function(event) {
                console.log("WebSocket connection closed", event);
            };

            ws.onerror = function(event) {
                console.error("WebSocket error observed:", event);
            };

            function sendMessage(event) {
                var input = document.getElementById("messageText");
                ws.send(input.value);
                input.value = '';
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

async def parser_ready(parser):
    cnt = 0
    while not parser.ready and cnt <= 200:
        await asyncio.sleep(0.8)
        cnt += 1
    return parser.ready

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    await websocket.send_json({})  # 웹소켓 연결을 유지합니다.

    try:
        async with VideoFinder() as finder:
            while True:
                try:
                    data = await websocket.receive_text()
                    response = await finder.find_urls(data)
                    await websocket.send_json(response)
                except asyncio.TimeoutError:
                    break
                except WebSocketException:
                    break
                except WebSocketDisconnect:
                    logging.info(f"Client {client_id} disconnected")
                    break

    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        if not websocket.client_state == WebSocketState.DISCONNECTED:
            await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
