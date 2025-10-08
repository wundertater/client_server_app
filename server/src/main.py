from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from server.src.api.departments.router import departments_route
from server.src.api.groups.router import groups_route
from server.src.api.instructors.router import instructors_route
from server.src.api.students.router import students_route
from server.src.dao.services import websockets_manager

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def home_page():
    return RedirectResponse(url="/docs")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websockets_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        websockets_manager.disconnect(websocket)


app.include_router(students_route)
app.include_router(instructors_route)
app.include_router(departments_route)
app.include_router(groups_route)
