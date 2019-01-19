# PythonMultiplayer

Simple multiplayer UDP server with Python

Boilerplate for basic UDP networking for simple python games

## Pre-req

Must have `Python 3+`
I'm currently not using any Python 3 features like async so it should be rather simple to backport to Python 2 if you want to

**Recommended**:
Install [pipenv](https://github.com/pypa/pipenv).
Project comes with a Pipfile. Simply run `pipenv install` to install dependencies and set up a virtualenv.

If you wish to use something like `virtualenv` and `pip` on it's own, feel free. Only dependency is `pygame` for display purposes.

## How to run

`git clone https://github.com/NoahBres/PythonMultiplayer`

**If you're using VSCode**:
Project comes with a .vscode `launch.json` so check those out. Simply select a debug profile.
`Server` launches the server. `Client 1` lauches the client with a UDP port of 1235. `Client 2` launches the client with a UDP port of 1236. `Server/Client` launches `Server` and `Client 1`. `Server/Client/Client` launches `Server`, `Client 1`, and `Client 2`. `Client1/Client2` launches both clients`

**Otherwise**:

_To launch server_:

1.  Navigate to `PythonMultiplayer/PythonMultiplayer/server`
2.  run `python -m server --tcpport 1234 --udpport 1234`

_To launch client_:

1.  Navigate to `PythonMultiplayer/PythonMultiplayer/client`
2.  run `python -m client --tcpport 1234 --udpport 1234 --socket 1235`

## Demo

![](assets/demo.gif)
