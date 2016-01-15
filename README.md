# ipaddressList
provides exclude- and superset-functions for python 3.3+ ipaddress(ip_network) lists,

I used this modules in order to calculate networks which were not used in a customer network.
Imagine you have lists with hundreds of prefixes which have been assigned and you want to 
calculate the prefixes which are unassigned:

    summaryNetwork = ip_network('192.168.178.0/24')
    nwList = ip_network_list([ip_network('192.168.178.0/26'),ip_network('192.168.178.64/27')])
    excludedNwList = nwList.exclude_from(summaryNetwork)
    >>> [IPv4Network('192.168.178.96/27'), IPv4Network('192.168.178.128/25')]
    
block_summarize does summarize the network in the list to blocks.
The prefix of the blocks is either user defined or calculated (min prefixlen of the contributing subnets)

    nwList = ip_network_list([ip_network('192.168.178.0/26'),ip_network('192.168.178.96/27')])
    summerizeBlockList = nwList.block_summarize(block_prefix=16)
    >>> [IPv4Network('192.168.178.0/16')]

supernet calculates the network with the longest prefix, which contains all network in the list

    nwList = ip_network_list([ip_network('192.168.178.0/26'),ip_network('192.168.0.128/25')] )
    supernetList = nwList.supernet()
    >>> 192.168.0.0/16

works for ipv4 and ipv6:

    summaryNetwork = ip_network('2001:db8::/56')
    myNwList = [ ip_network('2001:db8::/58'),ip_network('2001:db8:0:60::/59')]
    nwList = ip_network_list(myNwList)
    freeNetworkList = nwList.exclude_from(summaryNetwork)
    >>> [IPv6Network('2001:db8:0:40::/59'), IPv6Network('2001:db8:0:80::/57')]

    networkBlockList =[ip_network('2001:db8::/58'),ip_network('2001:db8:0:60::/59')]
    summerizeBlockList = nwList.block_summarize(block_prefix=56 )
    >>> [IPv6Network('2001:db8::/56')]

    summaryNetworks =[ip_network('2001:db8::/58'),ip_network('2001:db8:0:60::/59')]
    superNw = nwList.supernet()
    >>> 2001:db8::/57