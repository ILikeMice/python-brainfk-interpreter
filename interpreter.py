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
        self.loopstarts = [] # Keeps track of loop starts, aka '['
        self.loopends = [] # Does the same as self.lopstarts but for loopends (']')
        self.currentpointer = 0 # Current position in list of pointers, e.g. ([0][0]>[2]<[0][0]) (> and < as pointer)
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

    def expr(self): # Main logic, processes and fulfills the actual functions of the tokens
        output = ""
        usrinput = ""
        self.current_token = self.next_token()
        while self.current_token.type != EOF:

            if self.current_token.type == LOOPSTART and self.pos not in self.loopstarts:
                self.loopstarts.append(self.pos)
            
            if self.current_token.type == LOOPEND:

                if self.pos not in self.loopends:
                    self.loopends.append(self.pos)

                if self.memory[self.currentpointer] != 0:
                    self.pos = self.loopstarts[self.loopends.index(self.pos)]
                else:
                    self.loopstarts.pop(self.loopends.index(self.pos))
                    self.loopends.pop(self.loopends.index(self.pos))
            
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
