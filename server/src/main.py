from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get('/')
async def root(request: Request):
    return RedirectResponse(f'{request.url}docs')


@app.get('/students')
async def get_students():
    # фильтр
    # кафедра, группы, имя, фамилия
    ...


@app.get('/instructors')
async def get_instructors():
    # фильтр
    # кафедра, группы, имя, фамилия
    ...


@app.post('/invite_student')
async def invite_student():
    ...


@app.post('/invite_instructor')
async def invite_instructor():
    ...


@app.delete('delete_student')
async def delete_student():
    ...


