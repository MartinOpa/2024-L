import shlex

class Interpreter():
    def __init__(self):
        self.lines = []
        self.stack = []
        self.vars = {}

    def get_clean_input(self, input):
        if input.isdigit():
            return int(input)
        elif input.lower() == 'true':
            return True
        elif input.lower() == 'false':
            return False
        else:
            try:
                return float(input)
            except:
                return input

    def get_clean_value(self, cmd):
        if cmd[1] == 'I':
            return int(cmd[2])
        elif cmd[1] == 'F':
            return float(cmd[2])
        elif cmd[1] == 'S':
            return cmd[2]
        elif cmd[2] == 'true':
            return True
        else:
            return False
        
    def get_label_index(self, idx):
        for i in range(len(self.lines)):
            line = self.lines[i]
            params = shlex.split(line)

            if params[0] == 'label':
                if int(params[1]) == idx:
                    return i

            i += 1

    def perform_op(self, params):
        cmd = params[0]
        b = self.stack.pop()
        a = self.stack.pop()

        if cmd == 'add':
            res = a + b
        elif cmd == 'sub':
            res = a - b
        elif cmd == 'mul':
            res = a * b
        elif cmd == 'div':
            res = a / b
        elif cmd == 'mod':
            res = a % b
        elif cmd == 'concat':
            res = a + b
        elif cmd == 'and':
            res = a and b
        elif cmd == 'or':
            res = a or b
        elif cmd == 'gt':
            res = a > b
        elif cmd == 'lt':
            res = a < b
        elif cmd == 'eq':
            res = a == b

        self.stack.append(res)

    def process(self):
        i = 0
        while i < len(self.lines):
            line = self.lines[i]
            params = shlex.split(line)

            cmd = params[0]

            if cmd == 'push':
                val = self.get_clean_value(params)
                self.stack.append(val)
            elif cmd == 'pop':
                self.stack.pop()
            elif cmd == 'load':
                self.stack.append(self.vars[params[1]])
            elif cmd == 'save':
                self.vars[params[1]] = self.stack.pop()
            elif cmd == 'jmp':
                i = self.get_label_index(int(params[1]))
                continue
            elif cmd == 'fjmp':
                b_val = self.stack.pop()
                if not b_val:
                    i = self.get_label_index(int(params[1]))
                    continue
            elif cmd == 'print':
                out = ''
                for _ in range(int(params[1])):
                    out = str(self.stack.pop()) + out
                print(out)
            elif cmd == 'read':
                self.stack.append(self.get_clean_input(input()))
            elif cmd == 'uminus':
                val = self.stack.pop()
                self.stack.append(-val)
            elif cmd == 'not':
                val = self.stack.pop()
                self.stack.append(not val)
            elif cmd == 'itof':
                val = self.stack.pop()
                self.stack.append(float(val))
            elif cmd != 'label':
                self.perform_op(params)
                
            i += 1
