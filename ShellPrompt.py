from cmd import Cmd

class ShellPrompt(Cmd):
    prompt = 'it> '
    intro = "Welcome! Type ? to list commands"
    
    def do_exit(self, inp):
        '''exit the application. Shorthand q'''
        print("Bye")
        return True
    
    def do_say(self, inp):
        print("'{}'".format(inp))

    def help_exit(self):
        print("Safely exit the prompt. Shorthand: q")

    def help_say(self):
        print("Print the provided text")
    
    def default(self, inp):
        if inp == 'q':
            return self.do_exit(inp)
        print("Default: {}".format(inp))
    
ShellPrompt().cmdloop()
print("Exited shell")