from tkinter import *
from tkinter import messagebox
from textGenerator import RandomWordsGenerator
from datetime import datetime, timedelta


# Global game state
game_state = {
    'words_array': [],
    'score': 0,
    'end_time': None
}

# UI Components (initialized once)
window = Tk()
window.title('Typing Speed Test!')
window.minsize(width=1000, height=800)
window.config(padx=20, pady=20)

welcome_label = Label(text='Welcome to the type speed competition!', font=('Arial', 24, 'bold'))
welcome_label.grid(column=2, row=1)

# Display text box
text_box = Text(window, height=10, width=80, wrap=WORD, font=('Arial', 15), highlightthickness=5)
text_box.grid(column=2, row=2)

# Timer canvas
canvas = Canvas(width=500, height=400)
tomato_img = PhotoImage(file="./asset/tomato.png")
canvas.create_image(120, 130, image=tomato_img)
timer_text = canvas.create_text(120, 140, text="60", fill="white", font=('Arial', 35, "bold"))
canvas.grid(column=3, row=2)

# User text entry
user_text_entry = Text(window, width=80, height=10, highlightthickness=2, font=('Arial', 15), bg='lightblue')
user_text_entry.grid(column=2, row=3)


def reset_game():
    """Reset game state and UI for a new round"""
    game_state['words_array'] = RandomWordsGenerator().get_random_words(200)
    game_state['score'] = 0
    game_state['end_time'] = None
    
    # Update text box
    text_box.config(state=NORMAL)
    text_box.delete("1.0", END)
    text_box.tag_remove("highlight_word", "1.0", END)
    text_box.insert(END, " ".join(game_state['words_array']))
    text_box.config(state=DISABLED)
    
    # Clear user entry
    user_text_entry.delete("1.0", END)
    
    # Reset timer
    canvas.itemconfig(timer_text, text="60")


def check_game_start():
    """Check if user has started typing"""
    user_text = user_text_entry.get("1.0", "end-1c").strip()
    
    if user_text:
        print("Game start")
        game_state['end_time'] = datetime.now() + timedelta(seconds=60)
        game()
    else:
        window.after(500, check_game_start)


def highlight_word(word):
    """Highlight a word in the text box"""
    if not hasattr(highlight_word, 'configured'):
        text_box.tag_config("highlight_word", background="yellow")
        highlight_word.configured = True
    
    start_pos = text_box.search(word, "1.0", END)
    if start_pos:
        end_pos = f"{start_pos}+{len(word)}c"
        text_box.tag_add("highlight_word", start_pos, end_pos)


def game():
    """Main game loop - runs every 150ms during gameplay"""
    end_time = game_state['end_time']
    time_remaining = (end_time - datetime.now()).total_seconds()
    
    # Update timer display
    canvas.itemconfig(timer_text, text=str(max(0, int(time_remaining))))
    
    if datetime.now() < end_time:
        user_current_entry = user_text_entry.get("1.0", 'end-1c')
        last_word = user_current_entry.split()[-1] if user_current_entry else ""
        
        if last_word and last_word in game_state['words_array']:
            highlight_word(last_word)
            game_state['score'] += 1
        
        window.after(150, game)
    else:
        print(f"Game over! Score: {game_state['score']}")
        result = messagebox.askyesno(
            title="Game Over!",
            message=f"Game over, you got {game_state['score']} words in a minute.\nDo you wish to replay?"
        )
        if result:
            reset_game()
            check_game_start()
        else:
            window.quit()


# Start the game
reset_game()
check_game_start()

window.mainloop()