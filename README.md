
if input is server:
  socket = server socket
if input is client
  socket = client socket

boats = int***
def board = char***
off board = char***

def board get written the boat positions

com message = "action=position1-position2"
  - "hit=1,1"
  - "miss=1,1"
  - "sunken=1,1-1,2-1,3"

game loop until (send defeated) or (non empty mark on def board) or (non empty mark on off board)

S send postion
C goes through boats and mark miss/hit

C goes through the hit boat and checks if all pos is hit
  then marks all boat pos sunken

  C goes through all boats and check if all pos is sunken
    then send S "defeated" and ends their game

  C send S (all pos encoded) "sunken=1,1-1,2-1,3"

C send S action and position "hit=1,1" or "miss=1,1"

goes through all slots in def board:
  print out the state of the slot (empty, hit, miss, boat, sunken)
