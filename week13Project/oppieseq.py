"""

The Oppenheimer Sequence GUI is an interactive game that challenges players to decipher a 4-digit code before the
timer runs out. The game is inspired by historical events related to Robert Oppenheimer and his creation,
the bomb. Players are presented with a mysterious clue and must use their wit and intellect to prevent a chain
reaction by finding the correct code that stops the bomb.

Features:

-Timer: The game starts with a countdown timer of 15 seconds, adding excitement and urgency to the gameplay.
-Clues: Players receive clues that hint at the 4-digit code they need to crack to win the game.
-Numpad: The GUI provides a numpad for players to enter their guesses for the code.
-Keyboard Input: Players can use the keyboard for faster input:
    Enter digits (0-9) to input the code.
    Press 'p' or Enter Key to submit the code as PASS.
    Press 'c' or Backspace to clear the entered code (CLR).
    Press the spacebar to start the game.
-Play Button: When pressed, the 'Play' button initiates a new game round, showing a clue and starting the
              countdown timer.
-Exit Button: Players can exit the game at any time using the 'Exit' button.
-Result Display: The screen label displays the code result using asterisks ('****') to hide the code until guessed
                 correctly.
-Win and Fail Images: Depending on the outcome, the game displays victory or failure images to signify the player's
                      success or loss.
Gameplay:

The player presses the 'Play' button to start a new game round.
A clue is displayed, and the countdown timer starts.
The player uses the numpad buttons or the keyboard to enter their guess for the 4-digit code.
If the player guesses correctly before the timer runs out, they win, and a victory image is displayed.
If the player's guess is incorrect, they can continue guessing until the timer runs out.
If the timer runs out before the correct code is entered, the player loses, and a failure image is shown.
After each game round, the player can press "Play Again" to start a new round.
Enjoy the "Oppenheimer Sequence" GUI, and may your intellect become humanity's last hope in preventing the
bomb's impact!

Amidst the high-stakes scenario where the fate of the entire world hangs in the balance, one cannot simply exit
without consequence, for the game of life and death demands unwavering commitment. The exit button may be a mere
illusion, as once the game is set in motion, the weight of humanity's destiny rests upon your every move. A world on
the brink of chaos awaits your decision, and there's no turning back. In this thrilling quest to avert catastrophe,
your every action shapes the course of history, entwining your destiny with the pulse of the universe itself. """

import tkinter as tk
import random
from tkinter import messagebox

class OppieGUI:
    def __init__(self):
        # List of image filenames
        self.__image_list = ["bomb01.png", "bomb02.png", "bomb03.png",
                           "bomb04.png", "bomb05.png",
                           "bomb06.png", "bomb07.png", "bomb08.png",
                           "bomb09.png", "bomb10.png",
                           "bomb11.png", "bomb12.png", "bomb13.png",
                           "bomb14.png", "bomb15.png"]

        # Game instructions
        self.__init_game_instructions = "Welcome to 'The Oppenheimer Sequence' – a gripping journey in memory of " \
                                        "Robert Oppenheimer. Press 'Play' to reveal a mysterious clue and decipher a " \
                                        "4-digit code to stop the bomb he created, but never wanted to be unleashed. " \
                                        "Embrace the moment, and prevent regret from gripping the world. Use the " \
                                        "keyboard to:\n  - Enter digits (0-9) for the code.\n  - Press 'p' to submit " \
                                        "as PASS.\n  - Press 'c' to clear the code (CLR).\n  - Press spacebar to " \
                                        "start the game.\nGood luck in your quest! "


        self.__game_instructions = "When you press 'Play Again', a clue will be shown " \
                                   "here. Using the clue, you have to figure " \
                                   "out the 4-digit code to stop the bomb that " \
                                   "Oppenheimer created but never wanted to be " \
                                   "dropped on a country. Help him not regret, " \
                                   "before it is too late. \n\n" \
                                   "Remember to use the keyboard to enter the " \
                                   "code and submit it as PASS when ready."
        # Read answers from a file (not shown here)
        self.__answers = self.read_answers_from_file("answers.txt")

        # List of buttons and their positions
        self.__buttons = [
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2),
            ('0', 6, 0), ('CLR', 6, 1), ('PASS', 6, 2),
        ]

        # Initialize dynamic game variables
        ##Game rules
        self.__game_code = None
        self.__game_clue = ""
        self.__game_knowledge = ""
        self.__win = False
        self.__prev_code = None

        ##Time remaining in seconds
        self.__remaining_time = 0

        # Initialize static game variables
        self.__button_height = 5
        self.__button_width = 5

        ##Time to figure out the code
        self.__timeout = 15

        # Set the background and text color
        self.__bg_color = "black"
        self.__text_color = "#00FF00"

        # Create the main window
        self.root = tk.Tk()
        self.root.config(bg=self.__bg_color)
        self.root.title("OppieSeq")

        #Enabling the use of the keyboard
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<Return>", lambda event: self.on_button_click("PASS"))
        self.root.bind("<BackSpace>", lambda event: self.on_button_click("CLR"))
        self.root.bind("<space>", lambda event: self.start_timer())

        #Make the window full screen for a better experience
        self.root.attributes('-fullscreen', True)

        # Load the initial blank image (not shown here)
        self.__init_game_image = tk.PhotoImage(file="blank.png")
        self.__fail_image = tk.PhotoImage(file="boom.png")
        self.__mush_image = tk.PhotoImage(file="mushroom.png")
        self.__win_image = tk.PhotoImage(file="win.png")
        self.__open_image = tk.PhotoImage(file="open.png")

        # Timer running flag
        self.__timer_running = False

        # Title label
        self.title_label = tk.Label(self.root, text="THE OPPENHEIMER SEQUENCE",
                                    bg=self.__bg_color, fg=self.__text_color,
                                    font=("Montserrat", 14),
                                    highlightbackground="white")

        # Description label
        self.description_label = tk.Label(self.root,
                                          text="Crack the code before the "
                                               "time runs up",
                                          fg=self.__text_color, bg=self.__bg_color,
                                          font=("Arial", 12))

        # Screen label to display the code result
        self.result_var = tk.StringVar()
        self.result_var.set("****")
        self.screen_label = tk.Label(self.root, textvariable=self.result_var,
                                     fg=self.__text_color, bg=self.__bg_color,
                                     font=("Arial", 20), bd=5, relief="ridge",
                                     anchor="e")

        # Play button
        self.play_button = tk.Button(self.root, text="Play",
                                     font=("Arial", 16), fg=self.__text_color,
                                     bg=self.__bg_color, width=5 * 3, height=2,
                                     command=self.start_timer)

        # Exit button
        self.exit_button = tk.Button(self.root, text="Exit",
                                     font=("Arial", 16),
                                     fg=self.__text_color,
                                     bg=self.__bg_color,
                                     width=5 * 3,
                                     height=2,
                                     command=self.exit_game)

        # Timer label (not implemented)
        self.timer_label = tk.Label(self.root, text="", font=("Arial", 14),
                                    fg=self.__text_color, bg=self.__bg_color)

        # Big label to display game instructions
        self.clue_label = tk.Label(self.root, text=self.__init_game_instructions,
                                   font=("Times New Roman", 12),
                                   fg=self.__text_color, bg=self.__bg_color,
                                   wraplength=300, anchor="nw")



        # Create buttons and configure grid
        for button_text, row, col in self.__buttons:
            # Check if the button text is "PASS"
            if button_text == "PASS":
                button = tk.Button(self.root, text=button_text,
                                   font=("Montserrat", 10),
                                   width=self.__button_width, height=self.__button_height, fg="red",
                                   # Set foreground color to red
                                   bg=self.__bg_color,
                                   command=lambda
                                       text=button_text: self.on_button_click(
                                       text))
            else:
                button = tk.Button(self.root, text=button_text,
                                   font=("Montserrat", 10),
                                   width=self.__button_width, height=self.__button_height, fg=self.__text_color,
                                   bg=self.__bg_color,
                                   command=lambda
                                       text=button_text: self.on_button_click(
                                       text))

            button.grid(row=row, column=col, padx=1, pady=1)
            self.root.grid_columnconfigure(col, weight=1)
            self.root.grid_rowconfigure(row, weight=1)

        # Load the initial game image: Used for representing clues
        self.game_image_label = tk.Label(self.root, image=self.__init_game_image,
                                         bg=self.__bg_color, width=417,
                                         height=417)

        # Load the initial game image: Used for representing countdown
        # and win/fail
        self.image_label = tk.Label(self.root, image=self.__open_image,
                                    bg=self.__bg_color)

        #Positioning
        self.title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.description_label.grid(row=1, column=0, columnspan=3, padx=10,
                                    pady=5)
        self.screen_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.play_button.grid(row=7, column=3, padx=10, pady=10)
        self.exit_button.grid(row=8, column=3, padx=10, pady=10)
        self.timer_label.grid(row=9, column=3, columnspan=3)
        self.clue_label.grid(row=9, column=6, rowspan=4, columnspan=5, padx=10,
                             pady=10,sticky="e")
        self.game_image_label.grid(row=10, column=1, rowspan=5, padx=10,
                                   pady=10)
        self.image_label.grid(row=10, column=3, columnspan=1, padx=10, pady=10)

    def start_timer(self):
        """
        Starts the timer and initiates the game when the 'Play' button is
        pressed.
        :return: Does not return anything.
        """
        self.__win = False
        if not self.__timer_running and not self.__win:
            self.__timer_running = True
            self.play_game()
            self.play_button.config(state=tk.DISABLED)
            self.exit_button.config(state=tk.DISABLED)
            self.countdown(self.__timeout)

    def countdown(self, remaining):
        """
        Implements the countdown timer.
        :param remaining: int, the remaining time in seconds.
        :return: Does not return anything, but updates the timer and performs
                 actions when time is up.
        """
        if remaining <= 0:
            self.lose_game()
        else:
            self.__remaining_time = remaining
            self.timer_label.config(
                text=f"Estimated time for impact: {self.__remaining_time} "
                     f"second(s)")
            #Bomb drop animation
            self.BombImage = tk.PhotoImage(
                file=self.__image_list[15 - remaining])
            self.image_label.config(image=self.BombImage)
            self.timer_id = self.root.after(1000, self.countdown,
                                            remaining - 1)

    def stop_timer(self):
        """
        Stops the countdown timer.
        :return: Does not return anything.
        """
        if self.__timer_running:
            self.__timer_running = False
            self.root.after_cancel(self.timer_id)
            self.__win = True


    def on_button_click(self, text):
        """
        Handles button clicks during the game. :param text: str, the text on
        the button clicked. :return: Does not return anything, but updates
        the game based on button clicks.
        """
        if self.__timer_running:
            if text == 'PASS':
                if self.result_var.get() == str(self.__game_code):
                    self.win_game()
                else:
                    self.description_label.config(
                        text="Error: Wrong Code. Keep Trying")
                    self.result_var.set("****")
                pass
            elif text == 'CLR':
                self.result_var.set("****")
            elif self.result_var.get() != '****' and len(
                    self.result_var.get()) == 4:
                self.result_var.set("****")
                self.description_label.config(
                    text="Error: The code must be only 4 digits long")
            else:
                if self.result_var.get() == "****":
                    self.result_var.set(text)
                    self.description_label.config(
                        text="Crack the code before the time runs up")
                else:
                    self.result_var.set(self.result_var.get() + text)

    def play_game(self):
        """
        Starts a new game round.
        :return: Does not return anything.
        """

        #Trying to increase the level of randomness
        while True:
            random.shuffle(self.__answers)
            self.__game_code, self.game_image, self.__game_clue, self.__game_knowledge = \
                random.choice(self.__answers)

            if self.__game_code != self.__prev_code:
                break

            self.__prev_code = self.__game_code


        self.game_image = tk.PhotoImage(file=self.game_image)
        self.clue_label.config(text=self.__game_clue)
        self.clue_label.grid(row=1)
        self.clue_label.config(wraplength=500)
        self.game_image_label.config(image=self.game_image)

    def reset_game(self):
        """
        Resets the game state to its initial state after a game round ends.
        :return: Does not return anything.
        """

        self.result_var.set("****")
        self.__timer_running = False
        self.timer_label.config(text="")
        self.play_button.config(state=tk.NORMAL)
        self.exit_button.config(state=tk.NORMAL)
        self.clue_label.config(text=self.__game_instructions)
        self.clue_label.grid(row=9)
        self.clue_label.config(wraplength=300)
        self.image_label.config(image=self.__open_image)
        self.game_image_label.config(image=self.__init_game_image)
        self.play_button.config(text="Play Again")

    def exit_game(self):
        """
        Exits the game.
        :return: Does not return anything.
        """
        self.root.destroy()

    def read_answers_from_file(self, file_name):
        """
        Reads answers from a file and returns a list of answers.
        :param file_name: str, the filename of the file containing answers.
        :return: list, a list of answers.
        """
        answers_list = []
        with open(file_name, 'r') as file:
            for line in file:
                code, image, clue, info = line.strip().split(';')
                answers_list.append([code, image, clue, info])
        return answers_list

    def win_game(self):
        """
        Handles the actions when the player wins the game.
        Stops the timer, displays the win image, and shows a congratulatory message.
        Resets the game for the next play.
        :return: Does not return anything.
        """
        self.stop_timer()
        self.game_image_label.config(image=self.__win_image)
        messagebox.showinfo("Congratulations!",
                            f"You saved the world by {self.__remaining_time} "
                            f"second(s)!\n\n"
                            f"{self.__game_knowledge}")
        self.reset_game()

    def lose_game(self):
        """
        Handles the actions when the player loses the game (time's up).
        Stops the timer, sets buttons to normal state, displays the fail image,
        and shows a message indicating the failure.
        Resets the game for the next play.
        :return: Does not return anything.
        """
        self.__timer_running = False
        self.play_button.config(state=tk.NORMAL)
        self.exit_button.config(state=tk.NORMAL)
        self.image_label.config(image=self.__mush_image)
        self.game_image_label.config(image=self.__fail_image)
        messagebox.showinfo("Time's Up!",
                            f"History Repeats. The chain reaction has "
                            f"started.\n\n {self.__game_knowledge}")
        self.reset_game()

    def on_key_press(self, event):
        """
        Callback function for keypress events. This function is triggered
        whenever a key is pressed while the focus is on the main window.

        :param event: tk.Event, the event object representing the keypress event.
        """
        # Get the typed character from the event
        char = event.char

        # Check if the typed character is a digit or PASS/CLR
        if char.isdigit():
            self.on_button_click(char)
        elif char.lower() == 'p':
            self.on_button_click("PASS")
        elif char.lower() == 'c':
            self.on_button_click("CLR")





def main():
    oppie = OppieGUI()
    oppie.root.mainloop()


if __name__ == "__main__":
    main()
