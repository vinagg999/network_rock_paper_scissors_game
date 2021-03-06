import tkinter as tk
import socket
import threading
from time import sleep
import random


window = tk.Tk()
window.title("Sever")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Start", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Address: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.TOP, pady=(5, 10))

# PokerRound Frame for starting a round and showing table cards
# Dealer Options
pokerFrame = tk.Frame(window)
btnStartRound = tk.Button(pokerFrame, text="Start_Round", command=lambda : Start_Round())
btnStartRound.pack(side=tk.LEFT)
btnShowFlop = tk.Button(pokerFrame, text="Show_Flop", command=lambda : Show_Flop(),state=tk.DISABLED)
btnShowFlop.pack(side=tk.LEFT)
btnShowTurn = tk.Button(pokerFrame, text="Show_Turn", command=lambda : Show_Turn(),state=tk.DISABLED)
btnShowTurn.pack(side=tk.LEFT)
btnShowRiver = tk.Button(pokerFrame, text="Show_River", command=lambda : Show_River(),state=tk.DISABLED)
btnShowRiver.pack(side=tk.LEFT)
pokerFrame.pack(side=tk.BOTTOM, pady=(5, 10))


# End of dealer Options
server = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080
client_name = " "
clients = []
clients_names = []
player_data = []


# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT # code is fine without this
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print((socket.AF_INET))
    print((socket.SOCK_STREAM))

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Address: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


# Poker functions
total_cards = []
hands = {}
flops = []
turns = []
rivers = []

def make_deck():
    card_num = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    suit = ['C','S','D','H']

    for i in card_num:
        for j in suit:
            x = i+j
            total_cards.append(x)

def game_logic():
    global total_cards,hands,turns,flops,rivers

    if total_cards==[]:
        make_deck()

    random.shuffle(total_cards)
    player_num = len(clients)

    hands = {}
    flops = []
    turns = []
    rivers = []

    i = 0

    for a in clients:
        hands[a] = {}
        hands[a]["1"] = "./JPEG/"+total_cards[i] + ".jpg"
        hands[a]["2"] = "./JPEG/"+total_cards[i+player_num]+ ".jpg"
        i += 1

    i = 2*player_num+1

    for j in range(i,i+3):
        flops.append("./JPEG/"+total_cards[j]+ ".jpg")

    i += 4

    turns.append("./JPEG/"+total_cards[i]+ ".jpg")

    i +=2

    rivers.append("./JPEG/"+total_cards[i]+ ".jpg")

def Start_Round():

    game_logic()

    #code to distribute cards to the clients and show them only their cards

    for a in clients:
        a.send("hand1"+hands[a]["1"])
        # a.send("#")
        a.send("hand2"+hands[a]["2"])
        # a.send("#")

    btnStartRound.config(state=tk.DISABLED)
    btnShowFlop.config(state=tk.NORMAL)
    return

def Show_Flop():

    #code to display three cards to each client

    for a in clients:
        a.send("flop1"+flops[0])
        # a.send("#")
        a.send("flop2"+flops[1])
        # a.send("#")
        a.send("flop3"+flops[2])
        # a.send("#")


    btnShowFlop.config(state=tk.DISABLED)
    btnShowTurn.config(state=tk.NORMAL)
    return

def Show_Turn():

    #code to display fourth card to each client

    for a in clients:
        a.send("turn"+turns[0])
        # a.send("#")

    btnShowTurn.config(state=tk.DISABLED)
    btnShowRiver.config(state=tk.NORMAL)
    return

def Show_River():

    #code to display fifth card to each client and wait for round to get over

    for a in clients:
        a.send("river"+rivers[0])
        # a.send("#")

    btnShowRiver.config(state=tk.DISABLED)
    btnStartRound.config(state=tk.NORMAL)
    return

def accept_clients(the_server, y):
    while True:

        if len(clients) < 10:
            client, addr = the_server.accept()
            clients.append(client)

            # use a thread so as not to clog the gui thread
            threading._start_new_thread(send_receive_client_message, (client, addr))

# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, player_data, player0, player1

    client_msg = " "

    # send welcome message to client
    client_name = client_connection.recv(4096)
    client_connection.send("Welcome "+ client_name)
    clients_names.append(client_name)
    update_client_names_display(clients_names)


# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()
