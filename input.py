#!/usr/bin/env python3
import ipaddress
import dns.resolver
import time

#Function designed to validate IPv4 addresses
def validate_ip_address(dns_server):
    parts = dns_server.split(".")

    if len(parts) != 4:
        print("IP Address {} is not valid".format(dns_server))
        return False
    
    for part in parts:
        if not isinstance(int(part), int):
            print("IP address {} is not valid".format(dns_server))
            return False
        
        if int(part) < 0 or int(part) > 255:
            print("IP address {} is not valid".format(dns_server))
            return False

    print("DNS server is set to {}".format(dns_server))
    return True
     
            
#Main Section of the program
# Prompts user for input for specifying DNS server and text file of domains to lookup  
dns_server = input("What is the IP address of the DNS server?: ")
validate_ip_address(dns_server)
domains = input("Enter the full path of the file you wish to use for the domains: ")

#Declaring intiial variables and setting count iterator to 0
count = 0
my_resolver = dns.resolver.Resolver()
my_resolver.nameservers = [dns_server]


with open(domains) as filehandle:
    Lines = filehandle.readlines()
    for line in Lines:
        try:
            count += 1
            answer = my_resolver.query(line.strip(), 'A')
            for answers in answer:
                time.sleep(.5)  #Trying to limit the DNS query rate to not DOS the DNS server nor get blocked
                print('The IP address of {} is {}'.format(line, answers.to_text()))
                
        
        #Error Handling Section    
        except dns.resolver.NXDOMAIN:
            print ("Domain does not exist")
        except dns.resolver.Timeout:
            print ("TImed out")
        except dns.exception.DNSException:
            print ("Unspecified exception")