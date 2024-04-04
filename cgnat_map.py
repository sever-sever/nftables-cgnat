#!/usr/bin/env python3

"""
Script: cgnat.py
Author: Viacheslav Hletenko
Date: 2024
Description:
Generate nftables rules for CGNAT
Change external_prefix, internal_prefix and ports_per_user in the main()

Usage: python3 cgnat.py
       sudo nft -f cgnat.nft
"""
import ipaddress

BATCH_FILE_MAP_TEMPLATE = '''\
#!/usr/sbin/nft -f

add table ip {table_name}
flush table ip {table_name}

add map ip cgnat tcp_nat_map {{ type ipv4_addr: interval ipv4_addr . inet_service ; flags interval ;}}
add map ip cgnat udp_nat_map {{ type ipv4_addr: interval ipv4_addr . inet_service ; flags interval ;}}
add map ip cgnat icmp_nat_map {{ type ipv4_addr: interval ipv4_addr . inet_service ; flags interval ;}}
add map ip cgnat other_nat_map {{ type ipv4_addr: interval ipv4_addr ; flags interval ;}}
flush map ip cgnat tcp_nat_map
flush map ip cgnat udp_nat_map
flush map ip cgnat icmp_nat_map
flush map ip cgnat other_nat_map

table ip {table_name} {{
    map tcp_nat_map {{
        type ipv4_addr : interval ipv4_addr . inet_service
        flags interval
        elements = {{ {proto_map_elements} }}
    }}

    map udp_nat_map {{
        type ipv4_addr : interval ipv4_addr . inet_service
        flags interval
        elements = {{ {proto_map_elements} }}
    }}

    map icmp_nat_map {{
        type ipv4_addr : interval ipv4_addr . inet_service
        flags interval
        elements = {{ {proto_map_elements} }}
    }}

    map other_nat_map {{
        type ipv4_addr : interval ipv4_addr
        flags interval
        elements = {{ {other_map_elements} }}
    }}

    chain {chain_name} {{
        type nat hook {hook} priority {priority}; policy accept;
        ip protocol tcp counter snat ip to ip saddr map @tcp_nat_map
        ip protocol udp counter snat ip to ip saddr map @udp_nat_map
        ip protocol icmp counter snat ip to ip saddr map @icmp_nat_map
        counter snat ip to ip saddr map @other_nat_map
    }}
}}

'''

def execute_command(command):
    """PoC print only"""
    print(command)


class NftablesOperations:
    def __init__(
        self,
        table_name: str = 'cgnat',
        chain_name: str = 'POSTROUTING',
        hook: str = 'postrouting',
        priority: int = 100,
        interfaces: str = '',
        use_map: bool = False,
    ):
        self.table_name = table_name
        self.chain_name = chain_name
        self.hook = hook
        self.priority = priority
        self.interfaces = interfaces
        self.rules = []
        self.use_map = use_map
        self.proto_map_elements = ''
        self.other_map_elements = ''

    def add_table(self):
        execute_command(f'sudo nft add table ip {self.table_name}')

    def add_chain(self):
        execute_command(
            f'sudo nft add chain ip {self.table_name} {self.chain_name} {{ type nat hook {self.hook} priority {self.priority} \; policy accept \; }}'
        )

    def add_batch_rule(self, rule: str):
        self.rules.append(rule)

    def generate_batch_file(self) -> str:
        inbound_interfaces = ''
        if self.interfaces:
            inbound_interfaces = f'iifname {{ {self.interfaces} }}'

        # Generate the rules part of the template
        rules_content = ''
        for proto_map_element in self.proto_map_elements:
            rules_content += f'\n        {proto_map_element}'

        # Format the template with the necessary values
        content = BATCH_FILE_MAP_TEMPLATE.format(
            table_name=self.table_name,
            chain_name=self.chain_name,
            hook=self.hook,
            priority=self.priority,
            proto_map_elements=self.proto_map_elements,
            other_map_elements=self.other_map_elements,
        )

        return content

    def apply_rules(self):
        batch_file = self.generate_batch_file()
        with open('/tmp/cgnat.nft', 'w') as f:
            f.write(batch_file)
        execute_command(f'sudo nft -f /tmp/cgnat.nft')
        execute_command(f'sudo rm /tmp/cgnat.nft')


class IPOperations:
    def __init__(self, ip_prefix: str):
        self.ip_prefix = ip_prefix
        self.ip_network = ipaddress.ip_network(ip_prefix) if '/' in ip_prefix else None

    def get_ips_count(self) -> int:
        """Returns the number of IPs in a prefix or range.

        Example:
        % ip = IPOperations('192.0.2.0/30')
        % ip.get_ips_count()
        4
        % ip = IPOperations('192.0.2.0-192.0.2.2')
        % ip.get_ips_count()
        3
        """
        if '-' in self.ip_prefix:
            start_ip, end_ip = self.ip_prefix.split('-')
            start_ip = ipaddress.ip_address(start_ip)
            end_ip = ipaddress.ip_address(end_ip)
            return int(end_ip) - int(start_ip) + 1
        elif '/31' in self.ip_prefix:
            return 2
        elif '/32' in self.ip_prefix:
            return 1
        else:
            return sum(
                1
                for _ in [self.ip_network.network_address]
                + list(self.ip_network.hosts())
                + [self.ip_network.broadcast_address]
            )

    def convert_prefix_to_list_ips(self) -> list:
        """Converts a prefix or IP range to a list of IPs including the network and broadcast addresses.

        Example:
        % ip = IPOperations('192.0.2.0/30')
        % ip.convert_prefix_to_list_ips()
        ['192.0.2.0', '192.0.2.1', '192.0.2.2', '192.0.2.3']
        %
        % ip = IPOperations('192.0.0.1-192.0.2.5')
        % ip.convert_prefix_to_list_ips()
        ['192.0.2.1', '192.0.2.2', '192.0.2.3', '192.0.2.4', '192.0.2.5']
        """
        if '-' in self.ip_prefix:
            start_ip, end_ip = self.ip_prefix.split('-')
            start_ip = ipaddress.ip_address(start_ip)
            end_ip = ipaddress.ip_address(end_ip)
            return [
                str(ipaddress.ip_address(ip))
                for ip in range(int(start_ip), int(end_ip) + 1)
            ]
        elif '/31' in self.ip_prefix:
            return [
                str(ip)
                for ip in [
                    self.ip_network.network_address,
                    self.ip_network.broadcast_address,
                ]
            ]
        elif '/32' in self.ip_prefix:
            return [str(self.ip_network.network_address)]
        else:
            return [
                str(ip)
                for ip in [self.ip_network.network_address]
                + list(self.ip_network.hosts())
                + [self.ip_network.broadcast_address]
            ]


def generate_port_rules(
    external_hosts: list,
    internal_hosts: list,
    port_count: int,
    global_port_range: str = '1024-65535',
) -> list:
    """Generates list of nftables rules for the batch file."""
    rules = []
    proto_map_elements = []
    other_map_elements = []
    start_port, end_port = map(int, global_port_range.split('-'))
    total_possible_ports = (end_port - start_port) + 1

    # Calculate the required number of ports per host
    required_ports_per_host = port_count

    # Check if there are enough external addresses for all internal hosts
    if required_ports_per_host * len(internal_hosts) > total_possible_ports * len(
        external_hosts
    ):
        raise ValueError("Not enough ports available for the specified parameters!")

    current_port = start_port
    current_external_index = 0

    for internal_host in internal_hosts:
        external_host = external_hosts[current_external_index]
        next_end_port = current_port + required_ports_per_host - 1

        # If the port range exceeds the end_port, move to the next external host
        while next_end_port > end_port:
            current_external_index = (current_external_index + 1) % len(external_hosts)
            external_host = external_hosts[current_external_index]
            current_port = start_port
            next_end_port = current_port + required_ports_per_host - 1

        # Ensure the same port is not assigned to the same external host
        if any(
            rule.endswith(f'{external_host}:{current_port}-{next_end_port}')
            for rule in rules
        ):
            raise ValueError("Not enough ports available for the specified parameters")

        proto_map_elements.append(f'{internal_host} : {external_host} . {current_port}-{next_end_port}')
        other_map_elements.append(f'{internal_host} : {external_host}')

        current_port = next_end_port + 1
        if current_port > end_port:
            current_port = start_port
            current_external_index += 1  # Move to the next external host

    return [proto_map_elements, other_map_elements]


def main():
    nft = NftablesOperations()
    nft.add_table()
    nft.add_chain()
    print('---')

    # Change the values to required values
    # external_prefix = "192.0.2.2-192.0.2.5"
    # external_prefix = "192.0.2.0/30"
    external_prefix: str = '192.168.122.222/32'
    internal_prefix: str = '100.64.0.0/28'
    ports_per_user: int = 2000
    global_port_range: str = '1024-65535'
    output_filename: str = 'cgnat.nft'

    external_count = IPOperations(external_prefix).get_ips_count()
    internal_count = IPOperations(internal_prefix).get_ips_count()
    external_hosts = IPOperations(external_prefix).convert_prefix_to_list_ips()
    internal_hosts = IPOperations(internal_prefix).convert_prefix_to_list_ips()

    try:
        proto_maps, other_maps = generate_port_rules(
            external_hosts, internal_hosts, ports_per_user, global_port_range
        )
        nft.proto_map_elements = ', '.join(proto_maps)
        nft.other_map_elements = ', '.join(other_maps)

        # Write rules to the file
        with open(output_filename, 'w') as file:
            file.write(nft.generate_batch_file())

        print('external hosts count:', external_count)
        # print('external hosts list:', external_hosts)
        print('internal hosts count', internal_count)
        # print('internal hosts list', internal_hosts)
        print('global port range:', global_port_range)
        print('ports per host count:', ports_per_user)
        print('---')
        print(f'To apply rules use: nft -f {output_filename}\n')
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()

