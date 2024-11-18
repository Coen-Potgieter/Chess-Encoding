
# Usage

Follow these steps to encrypt and decrypt a message using chess games:

### 1. Install necessary dependencies  

- Run the following command to set up the required dependencies:  
	```bash  
	make init  
	``` 

### 2. Set up necessary directories  

- Create a directory structure in `src/data/` for your specific folder:  
	```bash  
	make setup <folder_name>  
	```  

### 3. Edit your secret message  

- Open the file `src/data/<folder_name>/secret.txt` and add your secret message

### 4. Encrypt the message  
- Encrypt the contents of `secret.txt` into a chess game
- The moves will be stored in `src/data/<folder_name>/predefined-moves/moves.json`:  
	```bash  
	make encrypt <folder_name>  
	```  

### 5. Play the encrypted chess game  

- Set up two terminal sessions to simulate the chess game between two bots:  

	- **Session A**:  
		```bash  
		make play_a <folder_name>  
		```  
	
	- **Session B**:  
		```bash  
		make play_b <folder_name>  
		```  

- During the game, the moves will be played out and the game IDs will be saved in `src/data/<folder_name>/played-games/ids.json` for future use.  

### 6. Load the played games  

- Retrieve the played games from Lichess using the saved game IDs
	```bash  
	make load <folder_name>  
	```  
- These games will be stored as `.pgn` files in `src/data/<folder_name>/played-games/`

### 7. Decrypt the games  

- Decrypt the loaded games to recover the original message:  
	```bash  
	make decrypt <folder_name>  
	```  

### 8. View the decrypted message  
- The decrypted message will be available in:  
	```  
	src/data/<folder_name>/outp.txt  
	```  

