# nftables-cgnat
CGNAT rules for nftables
The script generates nft CGNAT rules and save them to the file `cgnat.nft` in the local directory.

Change options:
`external_prefix` - prefix or range of IP addresses
`internal_prefix` - prefix
`ports_per_user` - `int` in the `main()` function
For example:
```none
    external_prefix = "192.0.2.0/30"
    internal_prefix = "100.64.0.0/28"
    ports_per_user = 8000
    global_port_range = "1024-65535"
```

# Example:
```none
$ python3 cgnat.py
---
external hosts count: 4
internal hosts count 16
global port range: 1024-65535
ports per host count: 8000
---
To apply rules use: nft -f cgnat.nft

```
Check the generated file:
```none
$ cat cgnat.nft
#!/usr/sbin/nft -f

add table ip cgnat
flush table ip cgnat
table ip cgnat {
    chain POSTROUTING {
        type nat hook postrouting priority 100; policy accept;
        meta l4proto tcp ip saddr 100.64.0.0 counter snat to 192.0.2.0:1024-9023
        meta l4proto udp ip saddr 100.64.0.0 counter snat to 192.0.2.0:1024-9023
        ip saddr 100.64.0.0 counter snat to 192.0.2.0
        meta l4proto tcp ip saddr 100.64.0.1 counter snat to 192.0.2.0:9024-17023
        meta l4proto udp ip saddr 100.64.0.1 counter snat to 192.0.2.0:9024-17023
        ip saddr 100.64.0.1 counter snat to 192.0.2.0
        meta l4proto tcp ip saddr 100.64.0.2 counter snat to 192.0.2.0:17024-25023
        meta l4proto udp ip saddr 100.64.0.2 counter snat to 192.0.2.0:17024-25023
        ip saddr 100.64.0.2 counter snat to 192.0.2.0
        meta l4proto tcp ip saddr 100.64.0.3 counter snat to 192.0.2.0:25024-33023
        meta l4proto udp ip saddr 100.64.0.3 counter snat to 192.0.2.0:25024-33023
        ip saddr 100.64.0.3 counter snat to 192.0.2.0
        meta l4proto tcp ip saddr 100.64.0.4 counter snat to 192.0.2.0:33024-41023
        meta l4proto udp ip saddr 100.64.0.4 counter snat to 192.0.2.0:33024-41023
        ip saddr 100.64.0.4 counter snat to 192.0.2.0
        meta l4proto tcp ip saddr 100.64.0.5 counter snat to 192.0.2.0:41024-49023
        meta l4proto udp ip saddr 100.64.0.5 counter snat to 192.0.2.0:41024-49023
        ip saddr 100.64.0.5 counter snat to 192.0.2.0
        meta l4proto tcp ip saddr 100.64.0.6 counter snat to 192.0.2.0:49024-57023
        meta l4proto udp ip saddr 100.64.0.6 counter snat to 192.0.2.0:49024-57023
        ip saddr 100.64.0.6 counter snat to 192.0.2.0
        meta l4proto tcp ip saddr 100.64.0.7 counter snat to 192.0.2.0:57024-65023
        meta l4proto udp ip saddr 100.64.0.7 counter snat to 192.0.2.0:57024-65023
        ip saddr 100.64.0.7 counter snat to 192.0.2.0
        meta l4proto tcp ip saddr 100.64.0.8 counter snat to 192.0.2.1:1024-9023
        meta l4proto udp ip saddr 100.64.0.8 counter snat to 192.0.2.1:1024-9023
        ip saddr 100.64.0.8 counter snat to 192.0.2.1
        meta l4proto tcp ip saddr 100.64.0.9 counter snat to 192.0.2.1:9024-17023
        meta l4proto udp ip saddr 100.64.0.9 counter snat to 192.0.2.1:9024-17023
        ip saddr 100.64.0.9 counter snat to 192.0.2.1
        meta l4proto tcp ip saddr 100.64.0.10 counter snat to 192.0.2.1:17024-25023
        meta l4proto udp ip saddr 100.64.0.10 counter snat to 192.0.2.1:17024-25023
        ip saddr 100.64.0.10 counter snat to 192.0.2.1
        meta l4proto tcp ip saddr 100.64.0.11 counter snat to 192.0.2.1:25024-33023
        meta l4proto udp ip saddr 100.64.0.11 counter snat to 192.0.2.1:25024-33023
        ip saddr 100.64.0.11 counter snat to 192.0.2.1
        meta l4proto tcp ip saddr 100.64.0.12 counter snat to 192.0.2.1:33024-41023
        meta l4proto udp ip saddr 100.64.0.12 counter snat to 192.0.2.1:33024-41023
        ip saddr 100.64.0.12 counter snat to 192.0.2.1
        meta l4proto tcp ip saddr 100.64.0.13 counter snat to 192.0.2.1:41024-49023
        meta l4proto udp ip saddr 100.64.0.13 counter snat to 192.0.2.1:41024-49023
        ip saddr 100.64.0.13 counter snat to 192.0.2.1
        meta l4proto tcp ip saddr 100.64.0.14 counter snat to 192.0.2.1:49024-57023
        meta l4proto udp ip saddr 100.64.0.14 counter snat to 192.0.2.1:49024-57023
        ip saddr 100.64.0.14 counter snat to 192.0.2.1
        meta l4proto tcp ip saddr 100.64.0.15 counter snat to 192.0.2.1:57024-65023
        meta l4proto udp ip saddr 100.64.0.15 counter snat to 192.0.2.1:57024-65023
        ip saddr 100.64.0.15 counter snat to 192.0.2.1
    }
}

```

Check and apply rules:
```none
$ sudo nft -c -f cgnat.nft
$ sudo nft -f cgnat.nft
$ sudo nft list table ip cgnat
```
# Example with maps
```
$ ./cgnat_map.py
sudo nft add table ip cgnat
sudo nft add chain ip cgnat POSTROUTING { type nat hook postrouting priority 100 \; policy accept \; }
---
external hosts count: 4
internal hosts count 16
global port range: 1024-65535
ports per host count: 8000
---
To apply rules use: nft -f cgnat.nft


sever@sever:~/scripts/repos/nftables-cgnat$ cat cgnat.nft 
#!/usr/sbin/nft -f

add table ip cgnat
flush table ip cgnat

add map ip cgnat tcp_nat_map { type ipv4_addr: interval ipv4_addr . inet_service ; flags interval ;}
add map ip cgnat udp_nat_map { type ipv4_addr: interval ipv4_addr . inet_service ; flags interval ;}
add map ip cgnat icmp_nat_map { type ipv4_addr: interval ipv4_addr . inet_service ; flags interval ;}
add map ip cgnat other_nat_map { type ipv4_addr: interval ipv4_addr ; flags interval ;}
flush map ip cgnat tcp_nat_map
flush map ip cgnat udp_nat_map
flush map ip cgnat icmp_nat_map
flush map ip cgnat other_nat_map

table ip cgnat {
    map tcp_nat_map {
        type ipv4_addr : interval ipv4_addr . inet_service
        flags interval
        elements = { 100.64.0.0 : 192.0.2.0 . 1024-9023, 100.64.0.1 : 192.0.2.0 . 9024-17023, 100.64.0.2 : 192.0.2.0 . 17024-25023, 100.64.0.3 : 192.0.2.0 . 25024-33023, 100.64.0.4 : 192.0.2.0 . 33024-41023, 100.64.0.5 : 192.0.2.0 . 41024-49023, 100.64.0.6 : 192.0.2.0 . 49024-57023, 100.64.0.7 : 192.0.2.0 . 57024-65023, 100.64.0.8 : 192.0.2.1 . 1024-9023, 100.64.0.9 : 192.0.2.1 . 9024-17023, 100.64.0.10 : 192.0.2.1 . 17024-25023, 100.64.0.11 : 192.0.2.1 . 25024-33023, 100.64.0.12 : 192.0.2.1 . 33024-41023, 100.64.0.13 : 192.0.2.1 . 41024-49023, 100.64.0.14 : 192.0.2.1 . 49024-57023, 100.64.0.15 : 192.0.2.1 . 57024-65023 }
    }

    map udp_nat_map {
        type ipv4_addr : interval ipv4_addr . inet_service
        flags interval
        elements = { 100.64.0.0 : 192.0.2.0 . 1024-9023, 100.64.0.1 : 192.0.2.0 . 9024-17023, 100.64.0.2 : 192.0.2.0 . 17024-25023, 100.64.0.3 : 192.0.2.0 . 25024-33023, 100.64.0.4 : 192.0.2.0 . 33024-41023, 100.64.0.5 : 192.0.2.0 . 41024-49023, 100.64.0.6 : 192.0.2.0 . 49024-57023, 100.64.0.7 : 192.0.2.0 . 57024-65023, 100.64.0.8 : 192.0.2.1 . 1024-9023, 100.64.0.9 : 192.0.2.1 . 9024-17023, 100.64.0.10 : 192.0.2.1 . 17024-25023, 100.64.0.11 : 192.0.2.1 . 25024-33023, 100.64.0.12 : 192.0.2.1 . 33024-41023, 100.64.0.13 : 192.0.2.1 . 41024-49023, 100.64.0.14 : 192.0.2.1 . 49024-57023, 100.64.0.15 : 192.0.2.1 . 57024-65023 }
    }

    map icmp_nat_map {
        type ipv4_addr : interval ipv4_addr . inet_service
        flags interval
        elements = { 100.64.0.0 : 192.0.2.0 . 1024-9023, 100.64.0.1 : 192.0.2.0 . 9024-17023, 100.64.0.2 : 192.0.2.0 . 17024-25023, 100.64.0.3 : 192.0.2.0 . 25024-33023, 100.64.0.4 : 192.0.2.0 . 33024-41023, 100.64.0.5 : 192.0.2.0 . 41024-49023, 100.64.0.6 : 192.0.2.0 . 49024-57023, 100.64.0.7 : 192.0.2.0 . 57024-65023, 100.64.0.8 : 192.0.2.1 . 1024-9023, 100.64.0.9 : 192.0.2.1 . 9024-17023, 100.64.0.10 : 192.0.2.1 . 17024-25023, 100.64.0.11 : 192.0.2.1 . 25024-33023, 100.64.0.12 : 192.0.2.1 . 33024-41023, 100.64.0.13 : 192.0.2.1 . 41024-49023, 100.64.0.14 : 192.0.2.1 . 49024-57023, 100.64.0.15 : 192.0.2.1 . 57024-65023 }
    }

    map other_nat_map {
        type ipv4_addr : interval ipv4_addr
        flags interval
        elements = { 100.64.0.0 : 192.0.2.0, 100.64.0.1 : 192.0.2.0, 100.64.0.2 : 192.0.2.0, 100.64.0.3 : 192.0.2.0, 100.64.0.4 : 192.0.2.0, 100.64.0.5 : 192.0.2.0, 100.64.0.6 : 192.0.2.0, 100.64.0.7 : 192.0.2.0, 100.64.0.8 : 192.0.2.1, 100.64.0.9 : 192.0.2.1, 100.64.0.10 : 192.0.2.1, 100.64.0.11 : 192.0.2.1, 100.64.0.12 : 192.0.2.1, 100.64.0.13 : 192.0.2.1, 100.64.0.14 : 192.0.2.1, 100.64.0.15 : 192.0.2.1 }
    }

    chain POSTROUTING {
        type nat hook postrouting priority 100; policy accept;
        ip protocol tcp counter snat ip to ip saddr map @tcp_nat_map
        ip protocol udp counter snat ip to ip saddr map @udp_nat_map
        ip protocol icmp counter snat ip to ip saddr map @icmp_nat_map
        counter snat ip to ip saddr map @other_nat_map
    }
}

```

Apply rules:
```
# nft -f cgnat.nft

# nft -s list table ip cgnat
table ip cgnat {
	map tcp_nat_map {
		type ipv4_addr : interval ipv4_addr . inet_service
		flags interval
		elements = { 100.64.0.0 : 192.0.2.0 . 1024-9023, 100.64.0.1 : 192.0.2.0 . 9024-17023,
			     100.64.0.2 : 192.0.2.0 . 17024-25023, 100.64.0.3 : 192.0.2.0 . 25024-33023,
			     100.64.0.4 : 192.0.2.0 . 33024-41023, 100.64.0.5 : 192.0.2.0 . 41024-49023,
			     100.64.0.6 : 192.0.2.0 . 49024-57023, 100.64.0.7 : 192.0.2.0 . 57024-65023,
			     100.64.0.8 : 192.0.2.1 . 1024-9023, 100.64.0.9 : 192.0.2.1 . 9024-17023,
			     100.64.0.10 : 192.0.2.1 . 17024-25023, 100.64.0.11 : 192.0.2.1 . 25024-33023,
			     100.64.0.12 : 192.0.2.1 . 33024-41023, 100.64.0.13 : 192.0.2.1 . 41024-49023,
			     100.64.0.14 : 192.0.2.1 . 49024-57023, 100.64.0.15 : 192.0.2.1 . 57024-65023 }
	}

	map udp_nat_map {
		type ipv4_addr : interval ipv4_addr . inet_service
		flags interval
		elements = { 100.64.0.0 : 192.0.2.0 . 1024-9023, 100.64.0.1 : 192.0.2.0 . 9024-17023,
			     100.64.0.2 : 192.0.2.0 . 17024-25023, 100.64.0.3 : 192.0.2.0 . 25024-33023,
			     100.64.0.4 : 192.0.2.0 . 33024-41023, 100.64.0.5 : 192.0.2.0 . 41024-49023,
			     100.64.0.6 : 192.0.2.0 . 49024-57023, 100.64.0.7 : 192.0.2.0 . 57024-65023,
			     100.64.0.8 : 192.0.2.1 . 1024-9023, 100.64.0.9 : 192.0.2.1 . 9024-17023,
			     100.64.0.10 : 192.0.2.1 . 17024-25023, 100.64.0.11 : 192.0.2.1 . 25024-33023,
			     100.64.0.12 : 192.0.2.1 . 33024-41023, 100.64.0.13 : 192.0.2.1 . 41024-49023,
			     100.64.0.14 : 192.0.2.1 . 49024-57023, 100.64.0.15 : 192.0.2.1 . 57024-65023 }
	}

	map icmp_nat_map {
		type ipv4_addr : interval ipv4_addr . inet_service
		flags interval
		elements = { 100.64.0.0 : 192.0.2.0 . 1024-9023, 100.64.0.1 : 192.0.2.0 . 9024-17023,
			     100.64.0.2 : 192.0.2.0 . 17024-25023, 100.64.0.3 : 192.0.2.0 . 25024-33023,
			     100.64.0.4 : 192.0.2.0 . 33024-41023, 100.64.0.5 : 192.0.2.0 . 41024-49023,
			     100.64.0.6 : 192.0.2.0 . 49024-57023, 100.64.0.7 : 192.0.2.0 . 57024-65023,
			     100.64.0.8 : 192.0.2.1 . 1024-9023, 100.64.0.9 : 192.0.2.1 . 9024-17023,
			     100.64.0.10 : 192.0.2.1 . 17024-25023, 100.64.0.11 : 192.0.2.1 . 25024-33023,
			     100.64.0.12 : 192.0.2.1 . 33024-41023, 100.64.0.13 : 192.0.2.1 . 41024-49023,
			     100.64.0.14 : 192.0.2.1 . 49024-57023, 100.64.0.15 : 192.0.2.1 . 57024-65023 }
	}

	map other_nat_map {
		type ipv4_addr : interval ipv4_addr
		flags interval
		elements = { 100.64.0.0 : 192.0.2.0/32, 100.64.0.1 : 192.0.2.0/32,
			     100.64.0.2 : 192.0.2.0/32, 100.64.0.3 : 192.0.2.0/32,
			     100.64.0.4 : 192.0.2.0/32, 100.64.0.5 : 192.0.2.0/32,
			     100.64.0.6 : 192.0.2.0/32, 100.64.0.7 : 192.0.2.0/32,
			     100.64.0.8 : 192.0.2.1/32, 100.64.0.9 : 192.0.2.1/32,
			     100.64.0.10 : 192.0.2.1/32, 100.64.0.11 : 192.0.2.1/32,
			     100.64.0.12 : 192.0.2.1/32, 100.64.0.13 : 192.0.2.1/32,
			     100.64.0.14 : 192.0.2.1/32, 100.64.0.15 : 192.0.2.1/32 }
	}

	chain POSTROUTING {
		type nat hook postrouting priority srcnat; policy accept;
		ip protocol tcp counter snat ip to ip saddr map @tcp_nat_map
		ip protocol udp counter snat ip to ip saddr map @udp_nat_map
		ip protocol icmp counter snat ip to ip saddr map @icmp_nat_map
		counter snat ip to ip saddr map @other_nat_map
	}
}

```
