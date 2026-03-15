import argparse
from dataclasses import dataclass

from cowsay import cowsay, cowthink


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


@dataclass
class Cow:
    msg: str
    cow: str = "default"
    eyes: str = "oo"
    wrap: bool = True

    def __str__(self):
        return cowsay(self.msg, cow=self.cow, eyes=self.eyes, wrap_text=self.wrap)

    def think(self):
        return cowthink(self.msg, cow=self.cow, eyes=self.eyes, wrap_text=self.wrap)


def twocows(cow1: Cow, cow2: Cow) -> str:
    return halign_bot(str(cow1), str(cow2))


def twocows_think(cow1: Cow, cow2: Cow) -> str:
    return halign_bot(cow1.think(), cow2.think())


if __name__ == "__main__":
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

    cow1 = Cow(args.msg1, cow=args.f, eyes=args.e, wrap=not args.n)
    cow2 = Cow(args.msg2, cow=args.F, eyes=args.E, wrap=not args.N)

    print(twocows(cow1, cow2))
