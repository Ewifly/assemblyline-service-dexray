import sys, os, string
from pathlib import Path

def main():
    print(sys.argv[1])
    my_cmd = "perl dexray.pl" + " " + sys.argv[1]
    print(my_cmd)
    my_cmd_output = os.popen(my_cmd)
    print("===============")
    for path in Path("./").glob(sys.argv[1] + ".*"):
        print(path)
    print("===============")

    for line in my_cmd_output:
        print(line)

if __name__ == "__main__":
    main()