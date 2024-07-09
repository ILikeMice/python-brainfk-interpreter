import sys

EOF, PLUS, MINUS, RIGHT, LEFT, LOOPSTART, LOOPEND, INPUT, OUTPUT = "EOF", "PLUS", "MINUS", "RIGHT", "LEFT", "LOOPSTART", "LOOPEND", "INPUT", "OUTPUT"

class Token(object):
    def __init__(self, type, val):
        self.type = type # One of the types in line 3 (PLUS,MINUS, etc.)
        self.val = val # The tokens value, for example '+'

class Interpreter(object):
    def __init__(self, text):
        self.text = text # The input code
        self.pos = 0 # Current position in input code, e.g. "+++-++-++"
        self.current_token  = None # Current selected token
        self.loops = {} # Keeps track of loops
        self.looppointers = []
        self.currentpointer = 0 # Current position in list of pointers, e.g. ([0][0]>[0]<[0][0]) (> and < as pointer)
        self.memory = { # Maybe not the best way to do it, list of all cells and its values, e.g. the default is just '[0]'
                0: 0
            }

    def error(self, num): # Creates an rror with error number
        raise Exception(f'Error while interpreting (Errno:{num})')
    
    def next_token(self): # Proceeds to next token
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        match current_char:
            
            case "+":
                token = Token(PLUS, current_char)
                self.pos += 1
                return token
            
            case "-":
                token = Token(MINUS, current_char)
                self.pos += 1
                return token
            
            case ">":
                token = Token(RIGHT, current_char)
                self.pos += 1
                return token
            
            case "<":
                token = Token(LEFT, current_char)
                self.pos += 1
                return token
            
            case "[":
                token = Token(LOOPSTART, current_char)
                self.pos += 1
                return token
            
            case "]":
                token = Token(LOOPEND, current_char)
                self.pos += 1
                return token
            
            case ".":
                token = Token(OUTPUT, current_char)
                self.pos += 1
                return token
            
            case ",":
                token = Token(INPUT, current_char)
                self.pos += 1
                return token
            
        self.error(1)

    def findloops(self): # Does some magic to get all the loops and write them down
        used = []
        pointer = 0
        code = self.text
        for i in range(len(code)):
            starts,ends = 0,0
            if i < len(code):
                if code[i] == ">":
                    pointer += 1
                if code[i] == "<":
                    pointer -= 1
                if code[i] == "[" and i not in used:
                    for b in range(i,len(code)):
                        if b in used:
                            break
                        match code[b]:
                            case "[":
                                starts+=1
                            case "]":
                                ends+=1
                        if starts == ends:
                            self.loops[b] = i,pointer
                            used.append(i)
                            used.append(b)
                            break

    def expr(self): # Main logic, processes and fulfills the actual functions of the tokens
        self.findloops()
        #self.loopends.reverse()
        output = ""
        usrinput = ""
        self.current_token = self.next_token()
        while self.current_token.type != EOF:    
            if self.current_token.type == LOOPEND: 
                if self.pos-1 in self.loops:
                    if self.memory[self.loops[self.pos-1][1]] != 0 :
                        self.pos = self.loops[self.pos-1][0]
                   
            if self.current_token.type == PLUS:
                self.memory[self.currentpointer] += 1

            if self.current_token.type == MINUS:
                self.memory[self.currentpointer] -= 1
                
            if self.current_token.type == OUTPUT:
                output += (chr(self.memory[self.currentpointer]))

            if self.current_token.type == INPUT:
                if usrinput == "":
                    usrinput += input(">")
                self.memory[self.currentpointer] = ord(usrinput[0])
                usrinput = usrinput.replace(usrinput[0],"")
               
            if self.current_token.type == RIGHT:
                self.currentpointer += 1
                if not self.currentpointer in self.memory:
                    self.memory[self.currentpointer] = 0
            
            if self.current_token.type == LEFT:
                self.currentpointer -= 1
                if not self.currentpointer in self.memory:
                    self.memory[self.currentpointer] = 0

            self.current_token = self.next_token()
        return output

def main(file):
    with open(file) as readfile:
        global inputfile 
        inputfile = readfile.read()
    
    interpreter = Interpreter(inputfile)
    print(interpreter.expr())

if __name__ == '__main__':
    main(sys.argv[-1]) # Takes a file from the command line as input, something like "python3 main.py brainfk.bf"
