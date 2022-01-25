""" Template use to make GET and POST request
    against a target specified as first
    argument

    you can use the following option :

        -u <url> : the url of the target

        -f <file> : use a configuration file instead
                    of positionnal arguments for
                    headers, cookies and proxies.
                    This file is in json format.
                    See example_config.json

        -he <header> : headers to add in the request headers
                      in json format

        -pr <proxies> : a proxy to use in json format

                default config is
                {
                    "http" : "http://127.0.0.1:8080",
                    "https": "http://127.0.0.1:8080"
                }

        -po <post> : data to posts

        -c <cookies> : cookies to add in json format

"""

# Local Modules
import argparse
import json
import re
import sys

# External Modules
import colorama
import requests
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

    regex_tags = re.compile(r"((?!(\<\!\-\-(?:.|\n|\r)*?-->))\<[a-zA-Z0-9\S]*\>|"
                            r"\<(?!(!))[a-zA-Z0-9]*|\/\>)")
    regex_value = re.compile(r"(\".*?\"|\'.*?\')")
    regex_href = re.compile(r"(((?:https?://|www\d{0,3}[.]|"
                            r"[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|"
                            r"(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|"
                            r"(\([^\s()<>]+\)))*\)|"
                            r"[^\s`!()\[\]{};:'\".,<>?«»“”‘’])))")
    regex_attribute = re.compile(r"(\s[a-zA-Z]*(?:[\=]))")
    regex_comment = re.compile(r"(\<\!\-\-(?:.|\n|\r)*?-->)")

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
                    get_requests.py --url http://google.fr -pr "{'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}" -he "{'personnal_header':'test'}"
                """
    parser = argparse.ArgumentParser(epilog=help_usage,
                                    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-u", "--url",
                        help='Url to target.',
                        required=True)
    parser.add_argument("-f", "--file",
                        help='Use json config file instead of arguments')
    parser.add_argument("-pr", "--proxies",
                        help='list of proxies to use in json, \ndefault is http://127.0.0.1:8080',
                        const=proxies,
                        nargs="?")
    parser.add_argument("-po", "--post",
                        help='list of data to POST in json format',
                        const=None,
                        nargs="?")
    parser.add_argument("-c", "--cookies",
                        help='list of cookies to use in json format',
                        const=None)
    parser.add_argument("-he", "--headers",
                        help='list of headers to use in json format',
                        const=headers, nargs="?")
    args = parser.parse_args()

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

    ###########################
    #   CASE OF CONFIG FILE   #
    ###########################
    if args.file:
        with open(args.file, "r", encoding='utf-8') as config_file:
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
            cookies = args.cookies.replace("'", "\"")
            cookies = json.loads(args.cookies.replace('"', '\"'))
        else:
            cookies = None

        #############################
        #       PROXY SETTINGS      #
        #############################
        if args.proxies:
            proxies = args.proxies.replace("'", "\"")
            proxies = json.loads(proxies)
        else:
            proxies = None

        ############################
        #      HEADERS SETTINGS    #
        ############################
        if args.headers:
            headers = args.headers.replace("'", "\"")
            headers = json.loads(headers)
        else:
            headers = None

        #############################
        #       POST SETTINGS       #
        #############################
        if args.post:
            data = args.post.replace("'", "\"")
            data = json.loads(data)
        else:
            data = None


        action_to_do(url, headers, cookies, proxies, data)


def action_to_do(url, headers, cookies, proxies, data):
    """ Function where you write what
        you want to do here
    """

    if data is not None:
        response = requests.post(url, proxies=proxies, cookies=cookies, headers=headers, data=data, verify=False)
    else:
        response = requests.get(url, proxies=proxies, cookies=cookies, headers=headers, verify=False)
    html_code = colorize_html(response.text)

    print("=====================================================")
    # Headers
    for header in response.headers:
        color_blue = colorama.Fore.BLUE
        color_bright = colorama.Style.BRIGHT
        color_reset = colorama.Fore.RESET + colorama.Style.RESET_ALL

        if header == "Set-Cookie":
            color_cookie_value = colorama.Fore.MAGENTA+colorama.Style.BRIGHT
            regex_cookie_value = re.compile(r"(\=.*\;)")
            response.headers[header] = re.sub(regex_cookie_value,
                                              color_cookie_value + r"\1" + color_reset,
                                              response.headers[header])
        else:
            print(color_blue+color_bright+header+color_reset+" : "+response.headers[header])
    print()

    # Body
    print(html_code)


if __name__ == "__main__":
    main()
