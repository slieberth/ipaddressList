# ipaddressList
provides exclude- and superset-function for python 3.3+ ipaddress(ip_network) lists:

    summaryNetwork = ip_network('192.168.178.0/24')
    nwList = ip_network_list([ip_network('192.168.178.0/26'),ip_network('192.168.178.64/27')])
    excludedNwList = nwList.exclude_from(summaryNetwork)

    >>> [IPv4Network('192.168.178.96/27'), IPv4Network('192.168.178.128/25')]