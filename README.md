# nftables-cgnat
CGNAT rules for nftables
The script generates nft CGNAT rules and save them to the file `cgnat.nft` in the local directory.

Change `external_prefix`, `internal_prefix`, `ports_per_user` in the `main()` function
For example:
```none
    external_prefix = "192.0.2.0/30"
    internal_prefix = "100.64.0.0/28"
    ports_per_user = 8000
    global_port_range = "1024-65535"
```

Example of usage:
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
