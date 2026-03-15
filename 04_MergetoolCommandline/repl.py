import cmd
from shlex import split

from cowsay import Option, list_cows
from twocows import Cow, twocows, twocows_think


class CmdCows(cmd.Cmd):
    def do_list_cows(self, arg):
        """list_cows
        List available animals.
        """
        for cow in list_cows():
            print(cow)

    def do_make_bubble(self, arg):
        pass

    def do_cowsay(self, arg):
        """cowsay msg1 [animal {param=value}] reply msg2 [animal {param=value}]
        Print two animals' dialogue.

        arguments:
            msg(1,2)    each animal's lines
            animal      animal file, see list_cows
            parameters:
                eyes
                tongue
        """
        args = split(arg)
        try:
            delim = args.index("reply")
        except ValueError:
            self.do_help("cowsay")
            return
        if delim == 0 or delim == len(args) - 1:
            self.do_help("cowsay")

        Cow1 = self.parse_cow_args(args[:delim])
        Cow2 = self.parse_cow_args(args[delim + 1 :])
        print(twocows(Cow1, Cow2))

    def do_cowthink(self, arg):
        """cowthink msg1 [animal {param=value}] reply msg2 [animal {param=value}]
        Print two animals' internal monologues.

        arguments:
            msg(1,2)    each animal's lines
            animal      animal file, see list_cows
            parameters:
                eyes
                tongue
        """
        args = split(arg)
        try:
            delim = args.index("reply")
        except ValueError:
            self.do_help("cowthink")
            return
        if delim == 0 or delim == len(args) - 1:
            self.do_help("cowthink")

        Cow1 = self.parse_cow_args(args[:delim])
        Cow2 = self.parse_cow_args(args[delim + 1 :])
        print(twocows_think(Cow1, Cow2))

    def do_EOF(self, arg):
        return -1

    def parse_cow_args(self, args):
        msg = args[0]
        cow = "default"
        if len(args) > 1:
            cow = args[1]
        params = {
            param: value
            for (param, value) in [
                (arg.split("=")[0], arg.split("=")[1]) for arg in args[2:]
            ]
        }
        eyes = Option.eyes
        if "eyes" in params.keys():
            eyes = params["eyes"]
        tongue = Option.tongue
        if "tongue" in params.keys():
            tongue = params["tongue"]
        return Cow(msg, cow=cow, eyes=eyes, tongue=tongue)


if __name__ == "__main__":
    cmd = CmdCows()
    cmd.cmdloop()
