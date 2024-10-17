# Chess-Encoding


## Resources

- python-chess docs: [python-chess: a chess library for Python — python-chess 1.10.0 documentation](https://python-chess.readthedocs.io/en/latest/)
- lichess API docs: [Lichess.org API reference](https://lichess.org/api#tag/Challenges/operation/challengeAccept)


## things learnt

### Web sockets

- WebSockets provide bi-directional, real-time communication channel between a client (my bots) and a server (the lichess game)
- Avoids having to use GET requests to constantly poll to see if something has happened
- **How it works:**
    - Establish WebSocket connection 
    - The bot then listens for events via the WebSocket stream
    - When Bot B lets say gets notified that Bot A made a move then it makes its move
    - Continue through this loop until the game ends

- **Practically**
    - From `ChatGPT`
```python
import asyncio
import websockets

async def play_game():
    url = "wss://lichess.org/api/board/game/stream/{game_id}"  # Replace with actual game stream URL
    async with websockets.connect(url) as websocket:
        while True:
            # Wait for an event from Lichess (like a move)
            event = await websocket.recv()
            print(f"Received event: {event}")
            
            # Parse event and decide on the bot's next move
            # Send move to Lichess API if it's this bot's turn
            if is_bot_turn(event):
                move = decide_next_move(event)
                await make_move(move)

# Start the game
asyncio.get_event_loop().run_until_complete(play_game())
```
- Notes on above code:
    - We use the `websockets` library to establish WebSocket connection
    - We use the `asyncio` library to run different tasks in our program asynchronously
    - The code will wait on the `await` lines for a received message from the websocket
    - Of course we don't want our prgram to stall forever and wait for one of these lines so we use asynchronous programming to perform other tasks while we wait for messages
    - This approach using asynchronous would be useful for this use case but I'm doing a simpler approach

- **My Approach:**
    - To keep things uncomplicated and modular im gonna have two programs running in different terminals concurrently. 
    - One for Bot A and one for Bot B
    - Then I might use docker to run these together with one executable


## Progress so far

- Run Bot A first then Bot B
- Right now Bot A successfully cancels all challenges and aborts all games then challenges Bot B
- Then Bot B accepts the challenge
- Need to figure out workflow of now play the accepted game between the two bots
- Need to change things, right now im polling the stream and they don't like that
- so change workflow

## Notes

- would like to export the state of the game at each move but their API delays this request by 3 to 60 seconds to avoid cheating of some sort