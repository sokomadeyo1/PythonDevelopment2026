import argparse
from cowsay import cowsay


parser = argparse.ArgumentParser()

parser.add_argument("-e", type=str, default="oo")
parser.add_argument("-f", type=str, default="default")
parser.add_argument("-n", action="store_true")
parser.add_argument("msg1", type=str)

parser.add_argument("-E", type=str, default="oo")
parser.add_argument("-F", type=str, default="default")
parser.add_argument("-N", action="store_true")
parser.add_argument("msg2", type=str)

args = parser.parse_args()

cow1 = cowsay(args.msg1, cow=args.f, eyes=args.e, wrap_text=not args.n)
cow2 = cowsay(args.msg2, cow=args.F, eyes=args.E, wrap_text=not args.N)

print(cow1)
print(cow2)
