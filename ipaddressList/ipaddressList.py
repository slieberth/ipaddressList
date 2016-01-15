#!/usr/bin/env python

__author__ = "Stefan Lieberth"
__copyright__ = "Copyright 2016"
__credits__ = [""]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Stefan Lieberth"
__email__ = "stefan@lieberth.net"
__status__ = "beta"

from os import listdir
from datetime import date
import sys

from ipaddress import ip_network,ip_address,ip_interface
from ipaddress import IPv4Network,IPv4Address,IPv4Interface
from ipaddress import IPv6Network,IPv6Address,IPv6Interface
from ipaddress import summarize_address_range, collapse_addresses


class ip_network_list (list):

    def __init__(self,*args,**kwargs):
        list.__init__(self,*args,**kwargs)

    def _check (self):
        if len (self) == 0: return -1
        #print (len(self))
        #print (self)
        if len ( set([ x.version for x in self ])) > 1: return -2
        #print (set([ x.version for x in self ]))
        return 0

    def _min_prefixlen (self):
        prefixlen = 128
        #print ("1: " + str(prefixlen))
        for nw in self:
            if nw.prefixlen < prefixlen: prefixlen = nw.prefixlen
        #print (prefixlen)
        return prefixlen 

    def exclude_from(self,summaryNw):
        #print ("_exclude_from")
        #self.sort(list(self))
        freeNetworkList = [summaryNw]
        for thisNetwork in self:
            for i,freeNetwork in enumerate(freeNetworkList):
                if thisNetwork.overlaps(freeNetwork):
                    newFreeNetworkList = freeNetworkList[:i] + \
                                list(freeNetwork.address_exclude(thisNetwork)) + \
                                 freeNetworkList[i+1:]
                #print(newFreeNetworkList )
            freeNetworkList = newFreeNetworkList  
        freeNetworkList.sort()
        return freeNetworkList

    def supernet(self):
        if self._check()  == 0:
            prefixlen = self._min_prefixlen()
            #print (prefixlen )
            newPrefixNwList =  [ip_network(x).supernet(new_prefix=prefixlen) for x in self ]
            newNetworkList = list(collapse_addresses(newPrefixNwList))
            while len (newNetworkList) > 1:
                prefixlen = prefixlen - 1
                newPrefixNwList =  [ip_network(x).supernet(new_prefix=prefixlen) for x in self ]
                newNetworkList = (list(collapse_addresses(newPrefixNwList)))
            return newNetworkList[0] 

    def block_summarize(self,block_prefix=""):
        if self._check()  == 0:
            if block_prefix == "":
                prefixlen = self._min_prefixlen()
            else:
                prefixlen = block_prefix
            #print ("prefixlen: " + str(prefixlen))
            newPrefixNwList =  [ip_network(x).supernet(new_prefix=prefixlen) for x in self ]
            return (list(collapse_addresses(newPrefixNwList)))


     

if __name__ == "__main__":

    print ("#"*40)
    summaryNetwork = ip_network('192.168.178.0/24')
    print ("summmary NW: " + str(summaryNetwork))
    myNwList = [ip_network('192.168.178.0/26'),ip_network('192.168.178.64/27')]
    nwList = ip_network_list(myNwList)
    nwList.sort()
    nwList.reverse()
    nwList.sort()
    print ("included NW    : " + str(nwList))
    #print ("check   : " + str(nwList._check()))
    freeNetworkList = nwList.exclude_from(summaryNetwork)
    print ("excluded NW    : " + str(freeNetworkList))
    print ("#"*40)
    networkBlockList = [  ip_network('192.168.178.0/26'),ip_network('192.168.178.64/27')]
    print ("NW Blocks: " + str(networkBlockList))
    nwList = ip_network_list(networkBlockList)
    summerizeBlockList = nwList.block_summarize()
    print ("summerized Blocks: " + str(summerizeBlockList))
    print ("#"*40)
    summaryNetworks = [  ip_network('192.168.178.0/26'),ip_network('192.168.0.128/25')]
    print ("summmary NWs: " + str(summaryNetworks))
    nwList = ip_network_list(summaryNetworks )
    supernetList = nwList.supernet()
    print ("supernet: " + str(supernetList))
    print ("#"*40)

    print ("#"*40)
    summaryNetwork = ip_network('2001:db8::/56')
    print ("summmary NW: " + str(summaryNetwork))
    myNwList = [ ip_network('2001:db8::/58'),ip_network('2001:db8:0:60::/59')]
    nwList = ip_network_list(myNwList)
    print ("used NW    : " + str(nwList))
    #print ("check   : " + str(nwList._check()))
    freeNetworkList = nwList.exclude_from(summaryNetwork)
    print ("free NW    : " + str(freeNetworkList))
    print ("#"*40)
    networkBlockList =[ip_network('2001:db8::/58'),ip_network('2001:db8:0:60::/59')]
    print ("NW Blocks: " + str(networkBlockList))
    nwList = ip_network_list( networkBlockList)
    summerizeBlockList = nwList.block_summarize(block_prefix=56 )
    print ("summerized Blocks: " + str(summerizeBlockList))
    print ("#"*40)
    summaryNetworks =[ip_network('2001:db8::/58'),ip_network('2001:db8:0:60::/59')]
    print ("summmary NWs: " + str(summaryNetworks))
    nwList = ip_network_list(summaryNetworks )
    supernetList = nwList.supernet()
    print ("supernet: " + str(supernetList))
    print ("#"*40)


