#!/usr/bin/env python
from ncclient import manager
from tabulate import tabulate
import env_lab

def get_int_info(host, username, password, port=830):
    net_dev = {
        'host': host,
        'port': port,
        'username': username,
        'password': password,
        'hostkey_verify': False
        }


    netconf_int_filter = """
	<filter>
	  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    	<interface/>
	  </interfaces>
	</filter>"""

	#Connect to device. Passing netowrk device using kwargs.
    with manager.connect(**net_dev) as m:
        netconf_reply = m.get_config(source = 'running', filter = netconf_int_filter)

    int_xml_inf = netconf_reply.data_ele

    interface_list = []

    for interface in int_xml_inf.getchildren()[0].getchildren():
        tmp_dict = {}
        tmp_dict['if_name'] = interface.find('./{*}name').text
        tmp_dict['if_type'] = interface.find('./{*}type').text
        tmp_dict['if_enabled'] = interface.find('./{*}enabled').text
        interface_list.append(tmp_dict)

    return interface_list

def pprint_interfaces(interfaces):
    headers = [
        'Interface name',
        'Interface type',
        'Interface enabled'
        ]

    table = []
    for intf in interfaces:
        tmp_entry = [
            intf['if_name'],
            intf['if_type'],
            intf['if_enabled']
            ]
        table.append(tmp_entry)

    print_str = tabulate(table, headers=headers, tablefmt='fancy_grid')
    print(print_str)




if __name__ == "__main__":
    my_device = {
        'host': env_lab.IOS_XE_1["host"],
        'port': env_lab.IOS_XE_1["netconf_port"],
        'username': env_lab.IOS_XE_1["username"],
        'password': env_lab.IOS_XE_1["password"]
		}

    interfaces = get_int_info(**my_device)

    pprint_interfaces(interfaces)
