# 🐍 term_snake 🐍
A python implementation of the classic snake game running in your terminal.
Made for the fun of it, as simple as it gets.

**This is the `silent version`. Please check the other branch if you're interested in playing with sound (Linux only)!**

To execute the game:
`python3 snake.py`

You can also add the game to your system PATH using `ln -s $PATH_TO_REPO/snake.py ~/.local/bin/snake`
and play the game simply by running `snake` in your terminal!

Use `W A S D` or the `arrow keys` to control your snek 🐍
Press the `p` key to pause the game.

Watchout for the ghost! 👻

~~I wish it could be run without **sudo**...~~
It no longer relies on the `keyboard` library.
It's been since implemented using `ncurses` for input processing and UI.
