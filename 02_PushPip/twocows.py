import argparse
from cowsay import cowsay


def halign_bot(text_l: str, text_r: str) -> str:
    """Align two multiline strings by the bottom."""
    lines_l = text_l.split("\n")
    lines_r = text_r.split("\n")
    wl = max(map(len, lines_l))
    hl = len(lines_l)
    hr = len(lines_r)

    pad_l = (hr - hl) * [""] + lines_l
    pad_r = (hl - hr) * [""] + lines_r
    lines_joined = list(map(lambda l, r: f"{l:{wl}} {r}", pad_l, pad_r))
    return "\n".join(lines_joined)


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

print(halign_bot(cow1, cow2))
