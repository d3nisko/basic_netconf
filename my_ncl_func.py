def get_int_info(net_dev):
    with manager.connect(**net_dev) as m:
        netconf_reply = m.get_config(source = 'running', filter = netconf_filter)
    int_xml_inf = netconf_reply.data_ele
    for interface in int_xml_inf.getchildren()[0].getchildren():
        if_name = interface.find('./{*}name').text
        if_type = interface.find('./{*}type').text
        if_enabled = interface.find('./{*}enabled').text
        print('Interface: {}, Type: {}, Enabled: {}'.format(if_name, if_type, if_enabled))