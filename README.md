# The program checks the status of your works 

[The program checks the status of your works](https://dvmn.org/)

## How to install

Python3 should already be installed. 
Use pip or pip3, if there is a conflict with Python2) to install dependencies:

- Installed [Docker Desktop](https://www.docker.com/)

#### Clone project
```
git clone git@github.com:rkinwork/devman-bot.git
```

```
pip install -r requirements.txt
```

## Program uses an environment variable

#### Variables:

`DVMN_TOKEN` Devman student's token.

`TG_BOT_TOKEN`  [bot token](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html)

`TG_CHAT_ID` `@userinfobot` возвращает значение твоего chat_id


## How to run scripts

```
python main.py
```

## deploy on server
#### Make file  /etc/systemd/system/api_devman.service
```service
 [Service]
 ExecStart=/opt/api_devman/env/bin/python3 /opt/api_devman/main.py
 Restart=always

 [Install]
 WantedBy=multi-user.target
```
Name of the service `api_devman`

You can easily run these commands
```bash
systemctl enable api_devman
systemctl start api_devman
systemctl stop api_devman
systemctl restart api_devman
```

After change the configuration
```bash
systemctl daemon-reload
```
## Create and start a container

```bash
docker build --tag api_devman .
```
#### start the container

```bash
docker run -d api_devman
```


## The aim of the project 
The code is written for educational purposes on the online course for web developers [Devman практика Python](https://dvmn.org/)
