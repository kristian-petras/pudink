# pudink
Cozy hypersocial game in Python.

## Requirements
How to run the client from the published build:
- Find latest artefact in the GitHub release and download Windows/Mac/Linux build.
- Install the game and play.

How to run the client from the repository:
- Have [pdm](https://pdm-project.org/en/latest/) installed.
- run ```pdm run client``` from root directory of the project.

How to run the server from the repository:
- Have [pdm](https://pdm-project.org/en/latest/) installed.
- run ```pdm run server``` from root directory of the project.

Issues:
- If ```pdm run``` does not work, try running ```pdm install``` or ```pdm venv activate``` beforehand.
- Otherwise, please consult [pdm](https://pdm-project.org/en/latest/) documentation.

## Implementation
Following section is a high level overview of client and server architecture, as well as some notes on key decisions that were made during implementation.
Project is split into three main packages.
- Common package contains API and translator for encoding and decoding messages between client and server. All messages that are communicated via network should be stored in common package.
- Client package contains Pyglet+Twisted application used by the player to connect to the server and interact with other players.
- Server package contains Twisted application used to mediate communication between players. It also handles registration and login.


### Client
Client uses Twisted for networking and Pyglet for rendering as the main dependencies. Both of the libraries control their own main loop,
so to be able to connect both libraries Pudink interleaves Pyglet ticks into Twisted main loop.

Structure of the client is composed of three main parts:
- renderer
- controller
- managers

### Server
