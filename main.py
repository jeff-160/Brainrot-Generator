__import__("sys").dont_write_bytecode = True

from args import parser
from generate import create_video

def main():
    args = parser.parse_args()

    if args.f:
        try:
            with open(args.f, mode="r", encoding="utf-8") as f:
                text = " ".join(f.readlines())
        except:
            print(f"Error: Could not locate file \"{args.f}\"")

    else:
        text = args.t

    create_video(text, args.o)

if __name__=="__main__":
    main()