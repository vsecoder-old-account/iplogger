import geoip2.database
import maxminddb.const

asn = geoip2.database.Reader(
    'mod/maxmind/GeoLite2-ASN.mmdb'
,   mode=maxminddb.const.MODE_MEMORY
)
city = geoip2.database.Reader(
    'mod/maxmind/GeoLite2-City.mmdb'
,   mode=maxminddb.const.MODE_MEMORY
)

def lookup(ip, user_agents):
    results = { "ip" : ip, "data": {} }

    try:    ip_city = city.city(ip)
    except: ip_city = None
    try:    ip_asn  = asn.asn(ip)
    except: ip_asn  = None

    ## ISP
    if ip_asn:
        ## ASN Database
        results['data']['aso'] = ip_asn.autonomous_system_organization or 'Unknown'
        results['data']['asn'] = str(ip_asn.autonomous_system_number or 'Unknown')

    ## Location
    if ip_city:
        ## Country Database
        results['data']['iso_code']       = str(ip_city.country.iso_code or 'Unknown')
        results['data']['continent_code'] = str(ip_city.continent.code or 'Unknown')
        results['data']['country']        = ip_city.country.name or 'Unknown'
        results['data']['continent']      = ip_city.continent.name or 'Unknown'

        ## City Database
        results['data']['zip_code']   = str(ip_city.postal.code or 'Unknown')
        results['data']['state']      = ip_city.subdivisions.most_specific.name or 'Unknown'
        results['data']['state_code'] = ip_city.subdivisions.most_specific.iso_code or 'Unknown'
        results['data']['city']       = ip_city.city.name or 'Unknown'
        results['data']['latitude']   = ip_city.location.latitude or 0.0
        results['data']['longitude']  = ip_city.location.longitude or 0.0
        results['user_agents']= user_agents
        results['error']      = False

        ## Author vsecoder
        #results['author']  = 'vsecoder'

    ## Dictionary with Valuable Data
    return results

def close():
    asn.close()
    city.close()