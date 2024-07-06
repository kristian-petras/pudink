# pudink
Cozy hypersocial game in Python.

TODO - showcase

## How to run

### Run the client from the published build
- Find latest artefact in the GitHub release and download Windows/Mac/Linux build.
- Install the game and play.

### Run the server from the published Dockerfile
- TODO

### Setup project
- Have [pdm](https://pdm-project.org/en/latest/) installed.
- Select interpreter by running ```pdm use```
- Activate virtual environment by running ```pdm venv activate```
- Install dependencies by running ```pdm install```

### Run the client from the repository
- Setup project.
- Run ```pdm run client``` from root directory of the project.

### Run the server from the repository
- Setup project.
- Run ```pdm run server``` from root directory of the project.

## Implementation
Following section is a high level overview of client and server architecture, as well as some notes on key decisions that were made during implementation.
Project is split into three main packages.
- Common package contains API and translator for encoding and decoding messages between client and server. All messages that are communicated via network should be stored in common package.
- Client package contains Pyglet+Twisted application used by the player to connect to the server and interact with other players.
- Server package contains Twisted application used to mediate communication between players. It also handles registration and login.


### Client
Client uses Twisted for networking and Pyglet for rendering as the main dependencies. Both of the libraries control their own main loop,
so to be able to connect both libraries Pudink interleaves Pyglet ticks into Twisted main loop.

Structure of the client is composed of following parts:
#### Assets
Contains assets such as character head/body, UI elements and background.

#### Controller
Contoller ensures the business logic of the game. Used to update the world state that is being rendered by the renderers.
Also used to switch scenes when the state of the game changes, e.g. disconnect by the server should switch you to the title screen.

#### Frontend
Is composed of utility classes to encapsulate some behaviour such as scene manager, asset manager or player display.
These are used to simplify drawing the correct sprites and batch groups. There is also custom implementation of Pyglet text entry to hide the password from being displayed.

#### Game
Package contains game factory that initializes the game state as well as backend clients to communicate with server.

#### Renderer
Renderers are responsible for drawing a scene from the game state.
They define labels, text entries, buttons, sprites and other UI elements that are displayed on the screen during the game loop.

### Common
Contains communication model between client and server. There is also translator included that can encode and decode the messages and provides a simple API to handle the messages.

### Server
Server uses Twisted for networking and Sqlite3 for user persistence.
Responsibility of the server is to handle connections, broadcast messages and enable player to register/login to the game server with the persisted state.

#### Database
Contains connector to Sqlite3 database which contains information about the user such as username, password, character head type and character body type.

#### Handler
Handlers are responsible for business logic of the game server. They are used to handle connection/disconnection routines and distribute updates about one player to other players.

#### Protocol
Contains implementation of Twisted protocol and required factories to create client connections and run the server.

## Repository
- Managed by ```pdm``` package manager.
- CI/CD pipelines via ```GitHub Actions```
- ```pyinstaller``` to create client distributions
- ```Docker``` to create server distribution
- ```black``` as the default formatter
- ```flake8/autoflake/pre-commit-hooks``` to ensure code quality

## Next steps
- Integrate logging framework
- Integrate configuration files
- Cleanup packages, add exports to ```__init__.py```
- Implement more features to the game
- Create and maintain integration/e2e tests
