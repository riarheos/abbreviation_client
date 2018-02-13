from termcolor import colored


def green(text):
    return colored(text, 'green', attrs=['bold'])


def yellow(text):
    return colored(text, 'yellow', attrs=['bold'])


def blue(text):
    return colored(text, 'blue', attrs=['bold'])


def red(text):
    return colored(text, 'red', attrs=['bold'])


def gray(text):
    return colored(text, 'white', attrs=['dark'])
