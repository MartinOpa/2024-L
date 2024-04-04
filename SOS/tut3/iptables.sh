#!/bin/bash

/sbin/iptables -A INPUT -i enp0s8 -p tcp --dport 22 -j ACCEPT
/sbin/iptables -A INPUT -i enp0s8 -p tcp --dport 2049 -j ACCEPT
/sbin/iptables -A INPUT -i enp0s8 -p udp --dport 2049 -j ACCEPT

/sbin/iptables -A OUTPUT -o enp0s8 -p tcp --sport 22 -j ACCEPT
/sbin/iptables -A OUTPUT -o enp0s8 -p tcp --sport 2049 -j ACCEPT
/sbin/iptables -A OUTPUT -o enp0s8 -p udp --sport 2049 -j ACCEPT

/sbin/iptables -A INPUT -p tcp --dport 80 -j ACCEPT
/sbin/iptables -A INPUT -p tcp --dport 443 -j ACCEPT
/sbin/iptables -A OUTPUT -p tcp --sport 80 -j ACCEPT
/sbin/iptables -A OUTPUT -p tcp --sport 443 -j ACCEPT 

/sbin/iptables -A INPUT -p icmp -j ACCEPT
/sbin/iptables -A OUTPUT -p icmp -j ACCEPT

/sbin/iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE

/sbin/iptables -A INPUT -j DROP
/sbin/iptables -A OUTPUT -j DROP 
