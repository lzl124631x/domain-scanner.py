from urllib.request import urlopen
import json
import threading
import sys, getopt

API_URL = "API_URL"

def getAvailability(urls):
    url = API_URL + ','.join(urls)
    content = urlopen(url)
    data = json.load(content)
    return data["status"]

def getUrls(names, endings):
    return [name + "." + ending for name in names for ending in endings]

def extractAvailable(status):
    return list(map(lambda x: x["name"], filter(lambda x: x["available"], status)))

def next(a):
    carry = 1
    index = -1
    while -index <= len(a) and carry:
        a[index] += 1
        carry = a[index] // 26
        a[index] %= 26
        index -= 1
    if carry:
        a.insert(0, 0)

def stringify(a):
    return ''.join([chr(ord("a") + ch) for ch in a])

def codify(s):
    return [ord(ch) - ord("a") for ch in s]

# https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval
def setInterval(func, sec):
    def funcWrapper():
        setInterval(func, sec)
        func()
    t = threading.Timer(sec, funcWrapper)
    t.start()
    return t

def getNamesAndEnd(start, count=40):
    code = codify(start)
    names = []
    for x in range(count):
        name = stringify(code)
        names.append(name)
        next(code)
    return (names, stringify(code))
            
def go():
    global start, endings
    names, start = getNamesAndEnd(start)
    urls = getUrls(names, endings)
    prefix = "from: %s, to: %s, " % (names[0], names[-1])
    try:
        a = getAvailability(urls)
        print("%savailable: %s" % (prefix, extractAvailable(a)), flush=True)
    except:
        print("%sFAILED" % prefix, flush=True)

def main(s, e, interval):
    global start, endings
    start = s
    endings = e
    print("start=%s, endings=%s, interval=%s" % (start, ",".join(endings), interval))
    setInterval(go, interval)

def parseArguments():
    # Default Values
    start = "a"
    endings = ["com"]
    interval = 1
    help = False
    # Parse
    unixOptions = "seih"  
    gnuOptions = ["start=", "endings=", "interval=", "help"]
    try:
        arguments, values = getopt.getopt(sys.argv[1:], unixOptions, gnuOptions)
        for arg, val in arguments:
            if arg in ("-s", "--start"):
                start = val
            elif arg in ("-e", "--endings"):
                endings = val.split(",")
            elif arg in ("-i", "--interval"):
                interval = int(val)
            elif arg in ("-h", "--help"):
                help = True
    except getopt.error as err:
        print("Failed to parse arguments.", str(err))
        sys.exit(2)
    return (start, endings, interval, help)

if __name__ == "__main__":
    args = parseArguments()
    if (args[-1]):
        print("-s, --start\tThe start string of domain name. Example: you want to search from \"abc.com\", set start to be \"abc\".")
        print("-e, --endings\tA list of Top Level Domains. Example: you are interested in \".com\" and \"io\", set endings to be \"com,io\".")
        print("-i, --interval\tThe interval of sending requests, in seconds. Example: you want request to be sent every 2 seconds, set interval to be 2.")
        print("-h, --help\tDisplay help messages.")
    else:
        main(*args[:-1])