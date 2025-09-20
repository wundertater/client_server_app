from fastapi import FastAPI

from server.src.api.instructor.router import instructors_route
from server.src.api.students.router import students_route

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "tmp"}


app.include_router(students_route)
app.include_router(instructors_route)
