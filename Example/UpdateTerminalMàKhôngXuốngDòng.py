import datetime
import time

# THAM KHẢO: https://tldp.org/HOWTO/Bash-Prompt-HOWTO/x361.html
# - Position the Cursor:
#   \033[<L>;<C>H
#      Or
#   \033[<L>;<C>f
#   puts the cursor at line L and column C.
# - Move the cursor up N lines:
#   \033[<N>A
# - Move the cursor down N lines:
#   \033[<N>B
# - Move the cursor forward N columns:
#   \033[<N>C
# - Move the cursor backward N columns:
#   \033[<N>D

# - Clear the screen, move to (0,0):
#   \033[2J
# - Erase to end of line:
#   \033[K

# - Save cursor position:
#   \033[s
# - Restore cursor position:
#   \033[u
       
# Print three lines of text
print("##########################")
print("Line 2")
print("##########################")

# Move cursor to beginning of first line
print("\033[2A", end="")

while True:
    # Get current time
    now = datetime.datetime.now()

    # Print time on first line and move cursor back
    print("[32;1m✓🧨🕛⏰⌚🕔[0m"+now.strftime("Time: %H:%M:%S"), end="\r")


    # Pause for 1 second
    time.sleep(1)
    print("\033[2K", end="")
