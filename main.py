import uvicorn
from src.apis import app
from src.initConfig import host, port

# run server
if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)