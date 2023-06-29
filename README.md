# Monopoly game
Play a simple monopoly. **Download the game from here: https://www.mediafire.com/file/8d73tqpjkd3sry3/Monopoly_game.exe/file**

## UI
For UI, I used raylib library.  
Link to raylib's website: www.raylib.com

## Programming language
I made this game using python programming language.

## How to use
The program has 2 windows. One shows the game, other show the information (errors, successes).  

**Fields**  
You can add your own field to the game. Title, description and points are required.  
Start adding fields with the index of 0. Then increase the index, or lower the index (if you want to insert a field).  

You can also load fields from a file.  
Supported formats are: **.json**, **.csv**, **.xls**, **.xlsx**  
Enter information in a file like this: title | description | points  
If your file has a **.xls** or **.xlsx** format, first line of a file will not be read. Put there anything you like.

**Deletion**  
"DEL ALL" button removes all fields from the board.  
"DEL I" and "DEL N" buttons remove a field by index or name, respectively.

## Game
Play a game till someone reaches "points to win" mark.  

**Change name**  
You can change your name by hovering over the default name with your mouse.

**Description**  
If description of the field is too long, the "..." will appear at the end of the description. Hover for 1 second with your mouse on the description you want to expand, and full description will appear.

**Someone won**  
When someone wins the game, you can press **Q** to move between monopoly board and prize podium.
