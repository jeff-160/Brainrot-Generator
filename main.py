__import__("sys").dont_write_bytecode = True

from args import parser
from generate import create_video

def main():
    args = parser.parse_args()

    if args.f:
        if args.f[::-1].find(".txt"[::-1]) != 0:
            raise Exception("Input file must be a .txt file")    
        
        try:
            with open(args.f, mode="r", encoding="utf-8") as f:
                text = " ".join(f.readlines())
        except:
            raise Exception(f"Could not locate file \"{args.f}\"")

    else:
        text = args.t

    create_video(text.replace("...", "."), args.o)

if __name__=="__main__":
    main()