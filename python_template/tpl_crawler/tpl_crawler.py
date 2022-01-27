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
    color_code_200 = colorama.Fore.GREEN
    color_code_400 = colorama.Fore.RED

    if "cookies" in options:
        cookies =  options["cookies"]

    if "headers" in options:
        headers =  options["headers"]

    if "proxies" in options:
        headers =  options["proxies"]

    for i in range(start, end):
        final_url = url+str(i)
        response = requests.get(final_url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            print(final_url + " : "+color_code_200 + str(response.status_code))


def crawl_list(url, wordlist, options):
    """ Function to crawl with a list of
        words specified in the -cl arguments
        of the command line
    """
    color_code_200 = colorama.Fore.GREEN
    color_code_400 = colorama.Fore.RED

    if "cookies" in options:
            cookies =  options["cookies"]

    if "headers" in options:
        headers =  options["headers"]

    if "proxies" in options:
        headers =  options["proxies"]

    with open(wordlist, 'r', encoding='utf-8') as wordlist:
        for word in wordlist.readlines():
            if not word.startswith("#"):
                word = word.rstrip()
                final_url = url+word
                response = requests.get(final_url, headers=headers, cookies=cookies)
                if response.status_code == 200:
                    print(final_url + " : "+color_code_200 + str(response.status_code))
                    print(word)

def main():
    """ MAIN FUNCTION
    """

    ####################
    # DEFAULT SETTINGS #
    ####################
    # Default Headers settings
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"
    }

    proxies = {
        "http" : "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }

    # ARGUMENTS
    help_usage = """Usages : \n
                    tpl_requests.py --url http://google.fr -pr "{'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}" -he "{'personnal_header':'test'}"
                    tpl_requests.py --url http://google.fr -he "{'personnal_header':'test'}" -s "<[a-z]{1,2}>"
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

    args = parser.parse_args()

    options =  {}
    options["headers"] = None
    options["cookies"] = None
    options["proxies"] = None
    if args.cookies:
        options["cookies"] = args.cookies
    if args.proxies:
        options["proxies"] = args.proxies
    if args.headers:
        options["headers"] = args.headers

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
