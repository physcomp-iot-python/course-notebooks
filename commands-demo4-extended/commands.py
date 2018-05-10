import sys

class CommandContext:
    def __init__(self, name, argv, output):
        self.name = name
        self.argv = argv
        self.nargs =  len(argv)
        self._output = output
        
    def print(self, text, endl='\n'):
        self._output.write(text)
        self._output.write(endl)

class CommandParser:
    def __init__(self, output = sys.stdout):
        self.commands = {}
        self._buffer = []
        self._print_func = print
        
    def attach(self, name, cmd_func):
        self.commands[name] = cmd_func
        
    def feed(self, data):
        endl_index = data.find('\n')
        if endl_index >= 0:                   #we detected a line ending
            #print("# found line ending")
            self._buffer.append(data[:endl_index])  #merge last of data
            line = "".join(self._buffer)            #and join the buffer
            self._buffer = [data[endl_index+1:]]    #put remainder in buffer
            #now parse the line by whitespace
            args = line.strip().split()
            #print("# args=%r"%args)
            #first arg is the command name, rest get passed in
            name = args[0]
            try:
                cmd = self.commands[name]
                #make a new context to pass into function
                context = CommandContext(name = name,
                                         argv = args[1:],
                                         print_func = self._print_func,
                                        )
                #print("# calling func: %r " % cmd)
                cmd(context)
            except KeyError:
                print("#ERROR: Invalid command: %s" % name)
        else:
            self._buffer.append(data)               #save the data so far
        #print("# %d bytes received: %r" % (num_rx,self._buffer))
