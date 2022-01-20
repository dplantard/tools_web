""" Template use to make GET request
    against a target specified as first
    argument

    you can use the following option :

        -u <url> : the url of the target

        -f <file> : use a configuration file instead
                    of positionnal arguments for
                    headers, cookies and proxies.
                    This file is in json format.
                    See example_config.json

        -h <header> : headers to add in the request headers
                      in json format

        -p <proxies> : a proxy to use in json format

                default config is 
                {
                    "http" : "http://127.0.0.1:8080",
                    "https": "http://127.0.0.1:8080"
                }

        -c <cookies> : cookies to add in json format

"""

import argparse
import colorama
import json
import re
import requests
import sys
import validators


def colorize_html(html_code):
    """ This function is used to colorize the following
    elements in html code :

        - tags
        - attributes & its values
        - href URL
        - comments
        
    """

    colorama.init(convert=True)
    color_tag = colorama.Fore.CYAN
    color_reset = colorama.Fore.RESET + colorama.Style.RESET_ALL
    color_attribute = colorama.Fore.CYAN + colorama.Style.BRIGHT
    color_comment = colorama.Fore.GREEN
    color_strings = colorama.Fore.YELLOW
    color_href = colorama.Fore.YELLOW + colorama.Style.BRIGHT

    regex_tags = re.compile(r"((?!(\<\!\-\-(?:.|\n|\r)*?-->))\<[a-zA-Z0-9\S]*>|\<(?!(!))[a-zA-Z0-9]*)")
    regex_value = re.compile(r"(\".*?\"|\'.*?\')")
    regex_href = re.compile(r"(((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])))")
    regex_comment = re.compile(r"(\<\!\-\-(?:.|\n|\r)*?-->)")
    regex_attribute = re.compile(r"(\s[a-zA-Z]*(?:[\=]))")

    # Colorize tags
    html_code = re.sub(regex_tags, color_tag + r"\1" + color_reset, html_code)

    # Colorize value
    html_code = re.sub(regex_value, color_strings + r"\1" + color_reset, html_code)

    # Colorize href
    html_code = re.sub(regex_href, color_href + r"\1" + color_reset, html_code)

    # Colorize attribute
    html_code = re.sub(regex_attribute, color_attribute + r"\1" + color_reset, html_code)

    # Colorize Comment
    html_code = re.sub(regex_comment, color_comment + r"\1" + color_reset, html_code)

    return html_code


def main(argv):

    ####################
    # DEFAULT SETTINGS #
    ####################
    # Default Headers settings
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0" 
    }

    proxyDict = {
        "http" : "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }


    # ARGUMENTS
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True)
    parser.add_argument("-f", "--file", help= 'Use json config file instead of arguments')
    parser.add_argument("-P", "--proxies", help='list of proxies to use in json format', const=proxyDict, nargs="?")
    parser.add_argument("-C", "--cookies", help='list of cookies to use in json format', const=None)
    parser.add_argument("-H", "--headers", help='list of headers to use in json format', const=headers, nargs="?")
    args = parser.parse_args()

    #############################
    #       URL FORMATTING      #
    #############################
    if args.url:
        url_format = validators.url(args.url)
        if url_format == True:
            url = args.url

        else:
            print("Invalid URL. Format is : http(s)://url.com")
            sys.exit()

    else:
        print("No URL Provided")
        sys.exit()

    ###########################
    #   CASE OF CONFIG FILE   #
    ###########################
    if args.file:
        print("config file choose")
        with open(args.file, "r") as config_file:
            configuration = json.load(config_file)
            for config in configuration:
                if config == "cookies":
                    cookies = configuration[config]
                if config == "proxies":
                    proxies = configuration[config]
                if config == "headers":
                    headers = configuration[config]

    else:
        #############################
        #      COOKIES SETTINGS     #
        #############################
        if args.cookies:
            cookies = args.cookies
        else:
            cookies = None

        #############################
        #       PROXY SETTINGS      #
        #############################
        if args.proxies:
            proxies = args.proxies
        else:
            proxies = None


    ###############################    
    # DO WHAT YOU WANT TO DO HERE #
    ###############################
    response = requests.get(url, proxies=proxies, cookies=cookies, headers=headers, verify=False)
    html_code = colorize_html(response.text)

    print("=====================================================")
    # Headers
    for header in response.headers:
        print(colorama.Fore.BLUE+colorama.Style.BRIGHT+header+colorama.Fore.RESET+" : "+response.headers[header])
    print()

    # Body
    print(html_code)


if __name__ == "__main__":
    main(sys.argv[1:])

