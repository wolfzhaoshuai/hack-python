#!/usr/bin/env python

'''
    locate position with module PyGeoIP
'''

import pygeoip
import optparse
from IPy import IP

gi=pygeoip.GeoIP('./geolitecity.dat')

def getlocation(tgt):
    rec=gi.record_by_name(tgt)
    if rec==None:
        print 'Unknown error'
        exit(0)
    city=rec['city']
    region=rec['region_code']
    country=rec['country_name']
    longitude=rec['longitude']
    lat=rec['latitude']
    print '[*] Target: '+tgt+' Geo-located'
    print '[+] '+str(city)+' '+str(region)+' '+str(country)
    print '[+] Latitude: '+str(lat)+', Longitude: '+str(longitude)

def main():
    optparser=optparse.OptionParser("Usage -H <DomainName/IP>")
    optparser.add_option('-H',dest='target',type='string')
    (options,args)=optparser.parse_args()
    tgt=options.target
    if tgt==None:
        print optparser.usage
        exit(0)
    ip=IP(tgt)
    if ip.iptype()=='PRIVATE':
        print '[-] %s is a private ip address' % tgt
        exit(0)
    else:
        getlocation(tgt)

if __name__=="__main__":
    main()
