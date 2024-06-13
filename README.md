# Test app for RLT

That test project i created for one day.

## For start

- create .env with MONGO_HOST, MONGO_PORT, BOT_TOKEN
- pip install -r requirements.txt

### First
- Go to /db
- To create docker container with mongodb that will upload test dump

```bash
docker build -t mongo .
```
- Up container with out logs

```bash
docker docker run -d --rm --name mongo -p 27017:27017 mongo:latest
```
- Congrats! We have Mongo with data on localhost:27017

### Second

- Start the app:

```bash
python main.py
```

