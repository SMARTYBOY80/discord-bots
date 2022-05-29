#If not on replit:
Install dependencies
```
python -m venv .venv
pyenv shell
pip install -r requirements.txt
```

Create Secrets file
```
mkdir bot_config
cd bot_config
touch secrets.json
secrets for "token", "mongo" and "DadjokeKey"
```

#If on replit:
Install dependencies
```
python -m venv .venv
pyenv shell
install requirements.txt through replit
```

Create secrets
```
change /bot_config/replit.json "onReplit" to "yes"
add secrets for "token", "mongo" and "DadjokeKey" through replit
```
