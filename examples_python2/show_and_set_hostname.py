#
# show_hostname.py
# version 1.0
#
# The purpose of this script is to show a server hostname
#
# written by: Check Point software technologies inc.
# July 2018
#

# A package for reading passwords without displaying them on the console.
from __future__ import print_function

import getpass

import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# lib is a library that handles the communication with the Check Point management server.
from cpapi import APIClient, APIClientArgs


def main():
    # getting details from the user
    api_server = raw_input("Enter server IP address or hostname:")
    username = raw_input("Enter username: ")
    if sys.stdin.isatty():
        password = getpass.getpass("Enter password: ")
    else:
        print("Attention! Your password will be shown on the screen!")
        password = raw_input("Enter password: ")

    client_args = APIClientArgs(server=api_server, api_version="1", unsafe=True, context="gaia_api")

    with APIClient(client_args) as client:

        # login to server:
        login_res = client.login(username, password)

        if login_res.success is False:
            print("Login failed: {}".format(login_res.error_message))
            exit(1)

        # request to show hostname
        api_res = client.api_call("show-hostname", {})
        if api_res.success:
            print("Hostname is '{}'".format(api_res.data["name"]))
        else:
            print("Failed to get hostname '{}'".format(api_res.data))

        # request to set hostname
        api_res = client.api_call("set-hostname", {"name": "Enter-new-hostname"})
        if api_res.success:
            print("Hostname name changed to '{}'".format(api_res.data["name"]))
        else:
            print("Failed to get hostname '{}'".format(api_res.data))


if __name__ == "__main__":
    main()
