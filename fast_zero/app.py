from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, users

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hello World</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                font-family: 'Arial', sans-serif;
            }
            .container {
                text-align: center;
                color: #fff;
            }
            h1 {
                font-size: 4em;
                animation: fadeIn 3s ease-in-out;
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Olá Mundo</h1>
        </div>
    </body>
    </html>
    """
