from tkinter import *
from tkinter import ttk, Tk
import json
from pathlib import Path

STATE_PATH = Path(__file__).with_name("state.json")
active_colour = "green"
poll_time = 5000

def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"yes": False, "no": False, "destroy": False}

def save_state(state):
    STATE_PATH.write_text(json.dumps(state, indent=2))

def check_state():
    new_state = load_state()
    if new_state != state:
        yes_button["bg"] = active_colour if new_state["yes"] else inactive_colour
        no_button["bg"] = active_colour if new_state["no"] else inactive_colour
        destroy_button["bg"] = active_colour if new_state["destroy"] else inactive_colour
    root.after(poll_time, check_state)

def toggle_colour(button, name):
    current_colour = button["bg"]
    if current_colour == inactive_colour:
        button["bg"] = active_colour
        state[name] = True 
    else:
        button["bg"] = inactive_colour
        state[name] = False
    save_state(state) 

def shutdown():
    state = {"yes": False, "no": False, "destroy": False}
    save_state(state)
    root.destroy()


root = Tk()
state = load_state()
frm = ttk.Frame(root, padding=10)
frm.grid(column=3, row=3)
ttk.Label(frm, text="LLM Testing").grid(column=1, row=0)
yes_button = Button(frm, text="Yes", command=lambda: toggle_colour(yes_button, "yes"))
yes_button.grid(column=0, row=1)
inactive_colour = yes_button["bg"]
no_button = Button(frm, text="No", command=lambda: toggle_colour(no_button, "no"))
no_button.grid(column=1, row=1)
destroy_button = Button(frm, text="Destroy All Humans", command=lambda: toggle_colour(destroy_button, "destroy"))
destroy_button.grid(column=2, row=1)
quit_button = Button(frm, text="Quit", command=lambda: shutdown()).grid(column=1, row=2)
root.after(poll_time, check_state)
root.mainloop()


