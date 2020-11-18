
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import socket
from time import sleep
import threading
from PIL import ImageTk, Image


# MAIN GAME WINDOW
window_main = tk.Tk()
window_main.title("Game Client")
your_name = ""
opponent_name = ""
game_round = 0
game_timer = 4
your_choice = ""
opponent_choice = ""
TOTAL_NO_OF_ROUNDS = 5
your_score = 0
opponent_score = 0

# network client
client = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080


#Connection Frame
top_welcome_frame= tk.Frame(window_main)
lbl_name = tk.Label(top_welcome_frame, text = "Name:")
lbl_name.pack(side=tk.LEFT)
ent_name = tk.Entry(top_welcome_frame)
ent_name.pack(side=tk.LEFT)
btn_connect = tk.Button(top_welcome_frame, text="Connect", command=lambda : connect())
btn_connect.pack(side=tk.LEFT)
top_welcome_frame.pack(side=tk.TOP)

#Welcome Frame
top_message_frame = tk.Frame(window_main)
lbl_line = tk.Label(top_message_frame, text="***********************************************************").pack()
lbl_welcome = tk.Label(top_message_frame, text="")
lbl_welcome.pack()
lbl_line_server = tk.Label(top_message_frame, text="***********************************************************")
lbl_line_server.pack_forget()
top_message_frame.pack(side=tk.TOP)

#Hand frame
button_frame = tk.Frame(window_main)

hand_1 = ImageTk.PhotoImage(file="rock.gif")
hand_2 = ImageTk.PhotoImage(file="rock.gif")

btn_hand_1 = tk.Button(button_frame, text="hand_1", command=lambda : choice("hand_1"), state=tk.DISABLED, image=hand_1)
btn_hand_2 = tk.Button(button_frame, text="hand_2", command=lambda : choice("hand_2"), state=tk.DISABLED, image=hand_2)
btn_hand_1.grid(row=0, column=0)
btn_hand_2.grid(row=0, column=1)
button_frame.pack(side=tk.TOP)


#table Frame
hand_frame = tk.Frame(window_main)
flop_1 = ImageTk.PhotoImage(file=r"rock.gif")
flop_2 = ImageTk.PhotoImage(file=r"rock.gif")
flop_3 = ImageTk.PhotoImage(file=r"rock.gif")
turn = ImageTk.PhotoImage(file=r"rock.gif")
river = ImageTk.PhotoImage(file=r"rock.gif")

btn_flop_1 = tk.Button(hand_frame, text="flop_1", command=lambda : choice("flop_1"), state=tk.DISABLED, image=flop_1)
btn_flop_2 = tk.Button(hand_frame, text="flop_2", command=lambda : choice("flop_2"), state=tk.DISABLED, image=flop_2)
btn_flop_3 = tk.Button(hand_frame, text="flop_3", command=lambda : choice("flop_3"), state=tk.DISABLED, image=flop_3)
btn_turn = tk.Button(hand_frame, text="turn", command=lambda : choice("turn"), state=tk.DISABLED, image=turn)
btn_river = tk.Button(hand_frame, text="river", command=lambda : choice("river"), state=tk.DISABLED, image=river)


btn_flop_1.grid(row=0, column=0)
btn_flop_2.grid(row=0, column=1)
btn_flop_3.grid(row=0, column=2)
btn_turn.grid(row=0, column=3)
btn_river.grid(row=0, column=4)

hand_frame.pack(side=tk.BOTTOM)


def connect():
    global your_name
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        your_name = ent_name.get()
        print(your_name)
        # lbl_your_name["text"] = "Your name: " + your_name
        connect_to_server(your_name)


def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, your_name
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name) # Send name to server after connecting

        btn_connect.config(state=tk.DISABLED)

        # start a thread to keep receiving message from server
        # do not block the main thread :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
    except Exception as e:
        tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")


def receive_message_from_server(sck, m):
    global your_name, opponent_name, game_round
    global your_choice, opponent_choice, your_score, opponent_score
    global btn_turn,btn_river,btn_flop_1,btn_flop_2,btn_flop_3,btn_hand_1,btn_hand_2

    while True:
        from_server = sck.recv(4096)

        if not from_server: break

        if from_server.startswith("welcome"):
            lbl_welcome["text"] = from_server + "! Game will start soon."
            lbl_line_server.pack()
        elif from_server.startswith("hand"):
            print(from_server)
            x = from_server.split('hand1')[1]
            y = x.split('hand2')

            btn_hand_1.config(image=ImageTk.PhotoImage(file="paper.gif"))
            btn_hand_2.config(image=ImageTk.PhotoImage(file="paper.gif"))

            print(y[0])
            print(y[1])


        elif from_server.startswith("flop"):
            print(from_server)
            x = from_server.split('flop1')[1]
            y = x.split('flop2')
            flop_1 = ImageTk.PhotoImage(Image.open(y[0]))
            z = y[1].split('flop3')
            flop_2 = ImageTk.PhotoImage(Image.open(z[0]))
            flop_3 = ImageTk.PhotoImage(Image.open(z[1]))
        elif from_server.startswith("turn"):
            print(from_server)
            file_name = from_server.replace("turn","")
            turn = ImageTk.PhotoImage(Image.open(file_name))
        elif from_server.startswith("river"):
            print(from_server)
            file_name = from_server.replace("river","")
            river = ImageTk.PhotoImage(Image.open(file_name))

    sck.close()


window_main.mainloop()
