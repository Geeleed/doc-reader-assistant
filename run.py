import uvicorn
from apis import app
from initConfig import host, port

# run server
if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)