import json


class logReader:
    def __init__(self,file_p):
        self.file_p = file_p
        self.turn_index=0

        with open(file_p,"r") as fp:
            read_in = fp.readlines()
        read_in.reverse()
        self.data = []
        curr_turn = []
        while len(read_in)>1:
            curr_item = read_in.pop()


            if curr_item == "\n":

                self.data.append(curr_turn.copy())
                curr_turn = []

            else:

                curr_turn.append(curr_item)
                #print(curr_turn)



    def nextTurn(self):
        self.turn_index+=1
        try:
            return self.data[self.turn_index-1]
        except:
            print("Reached end of log --log reader")
            return None



logReader("game.log").nextTurn()