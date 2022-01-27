""" Template use to crawl website in different ways

"""

# Local modules
import json
import re
import time

# External modules
import argparse
import colorama
import requests
import validators


def crawl_integer(url, start, end, options):
    """ Function to crawl with a range of
        integer specified in the -ci arguments
        of the command line
    """

    # Get options from command line
    if "cookies" in options:
        cookies = options["cookies"]

    if "headers" in options:
        headers = options["headers"]

    if "proxies" in options:
        proxies = options["proxies"]
    
    if "symbol" in options:
        symbol = options["symbol"]

    if "time" in options:
        time_throttle = float(options["time"])
    
    regex_sym = re.compile(symbol+".*"+symbol)

    for i in range(start, end):
        # Action
        action_to_do(response)
        time.sleep(time_throttle)


def crawl_list(url, wordlist, options):
    """ Function to crawl with a list of
        words specified in the -cl arguments
        of the command line
    """

    # Get options from command line
    if "cookies" in options:
            cookies =  options["cookies"]

    if "headers" in options:
        headers =  options["headers"]

    if "proxies" in options:
        headers =  options["proxies"]

    if "symbol" in options:
        symbol =  options["symbol"]

    if "time" in options:
        time_throttle = float(options["time"])

    regex_sym = re.compile(symbol+".*"+symbol)

    with open(wordlist, 'r', encoding='utf-8') as wordlist:
        for word in wordlist.readlines():
            if not word.startswith("#"):
                # Action
                # Build URL replacing pattern "°"
                action_to_do(response)
                time.sleep(time_throttle)


def action_to_do(final_url):
    """ function dedicated to the specific 
        action you need to do
    """
    # Colorize 
    color_code_200 = colorama.Fore.GREEN
    color_code_400 = colorama.Fore.RED
    color_reset = colorama.Fore.RESET + colorama.Style.RESET_ALL

    response = requests.get(final_url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        print(final_url + " : "+ color_code_200 + str(response.status_code)+color_reset)

def action_example():
    """ Example of function you can do
        inject the payload in headers, cookies
        and URL
    """
    final_headers = {}
    final_cookies = {}

    # Build Headers replacing pattern "°"
    if headers is not None:
        for header in headers:
            final_headers[header] = re.sub(regex_sym, word, headers[header])

    # Build Cookies replacing pattern "°"
    if cookies is not None:
        for cookies in cookies:
            final_cookies[cookie] = re.sub(regex_sym, word, cookies[cookie])

    # Build URL replacing pattern "°"
    word = word.rstrip()
    final_url = re.sub(regex_sym, word , url)
    response = requests.get(final_url, headers=headers, cookies=cookies)


def main():
    """ MAIN FUNCTION
    """

    ####################
    # DEFAULT SETTINGS #
    ####################
    # Default Headers settings
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/°96°.0"
    }

    proxies = {
        "http" : "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }

    # ARGUMENTS
    help_usage = """
                    Use the symbole "°" to specify the paramter/file/directory to crawl \n

                    Example : \n
                    tpl_crawler.py --url http://website.com/repos_°1° -ci 1-1000"
                    tpl_requests.py --url http://website.com/index.php?param=°parameter° -cl wordlist.txt"
                """
    parser = argparse.ArgumentParser(epilog=help_usage,
                                    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-u", "--url",
                        help='Url to target.',
                        required=True)
    parser.add_argument("-pr", "--proxies",
                        help='list of proxies to use in json, \ndefault is http://127.0.0.1:8080',
                        const=proxies,
                        nargs="?")
    parser.add_argument("-c", "--cookies",
                        help='list of cookies to use in json format',
                        const=None)
    parser.add_argument("-he", "--headers",
                        help='list of headers to use in json format',
                        const=headers, nargs="?")
    parser.add_argument("-ci", "--crawl_int",
                        help='crawl by integer')
    parser.add_argument("-cl", "--crawl_list",
                        help='crawl by integer')
    parser.add_argument("-cb", "--crawl_brute",
                        help='crawl by brute force')
    parser.add_argument("-sy", "--symbol",
                        help='symbole to delimit the crawling element (default is "°")')
    parser.add_argument("-t", "--time",
                        help='time in second between each request. Default is 0')

    args = parser.parse_args()

    options =  {}
    options["headers"] = None
    options["cookies"] = None
    options["proxies"] = None
    options["time"] = None
    options["symbol"] = "°"
    options["time"] = 0
    if args.cookies:
        cookies = args.cookies.replace("'", "\"")
        cookies = json.loads(args.cookies.replace('"', '\"'))
        options["cookies"] = cookies

    if args.proxies:
        proxies = args.proxies.replace("'", "\"")
        proxies = json.loads(proxies)
        options["proxies"] = proxies

    if args.headers:
        headers = args.headers.replace("'", "\"")
        headers = json.loads(headers)
        options["headers"] = headers

    if args.symbol:
        options["symbol"] = args.symbol
    if args.time:
        options["time"] = args.time

    #############################
    #       URL FORMATTING      #
    #############################
    if args.url:
        url_format = validators.url(args.url)
        if url_format is True:
            url = args.url

        else:
            print("Invalid URL. Format is : http(s)://url.com")
            sys.exit()

    else:
        print("No URL Provided")
        sys.exit()

    # Crawl integer
    if args.crawl_int:
        start = int(args.crawl_int.split("-")[0])
        end = int(args.crawl_int.split("-")[1])
        crawl_integer(url, start, end, options)

    # Crawl list
    elif args.crawl_list:
        wordlist = args.crawl_list
        crawl_list(url, wordlist, options)

if __name__ == "__main__":
    main()
