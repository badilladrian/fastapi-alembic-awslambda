from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.api import deps
from sqlalchemy.orm import Session
from app.cruds.notes import crud_note
from app.schemas.notes import Note
from .manager import ConnectionManager

router = APIRouter()

manager = ConnectionManager()


@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(deps.get_db_global)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            if not data.isnumeric():
                result = "Not a number"
            else:
                result = f"Note ID: {data} | "

                note = crud_note.get(db=db, id=int(data))
                if note:
                    note_dict = note.__dict__
                    note_dict.pop("_sa_instance_state")
                    result += str(note_dict)
                else:
                    result += "Not found"

            await manager.send_message(result, websocket)
    except WebSocketDisconnect:
        await manager.broadcast(f"Some Client Disconnected")


# Test Endpoint
from fastapi.responses import HTMLResponse
from app.core.config import settings

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Note</title>
    </head>
    <body>
        <h1>WebSocket Note</h1>
        <form action="" onsubmit="sendMessage(event)">
            <span>Note ID:</span>
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Query</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("{settings.API_HOST.replace("http://","ws://")}/v1/notes/ws/");
            ws.onmessage = function(event) {{
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            }};
            function sendMessage(event) {{
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }}
        </script>
    </body>
</html>
"""


@router.get("/test")
async def get():
    return HTMLResponse(html)
