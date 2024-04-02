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


def execute_command(command):
    print(command)


class NftablesOperations:
    def __init__(
        self,
        table_name: str = 'cgnat',
        chain_name: str = 'POSTROUTING',
        hook: str = 'postrouting',
        priority: int = 100,
        interfaces: str = '',
    ):
        self.table_name = table_name
        self.chain_name = chain_name
        self.hook = hook
        self.priority = priority
        self.interfaces = interfaces
        self.rules = []

    def add_table(self):
        execute_command(f'sudo nft add table ip {self.table_name}')

    def add_chain(self):
        execute_command(
            f'sudo nft add chain ip {self.table_name} {self.chain_name} {{ type nat hook {self.hook} priority {self.priority} \; policy accept \; }}'
        )

    def add_batch_rule(self, rule: str):
        self.rules.append(rule)

    # def get_rules(self):
    #     return self.rules
    #
    # def clear_batch_rules(self):
    #     self.rules = []

    def generate_batch_file(self) -> str:
        inbound_interfaces = ''
        if self.interfaces:
            inbound_interfaces = f'iifname {{ {self.interfaces} }}'
        content = '#!/usr/sbin/nft -f\n\n'
        content += f'add table ip {self.table_name}\n'
        content += f'flush table ip {self.table_name}\n'
        content += f'table ip {self.table_name} {{\n'
        content += f'    chain {self.chain_name} {{\n'
        content += f'        type nat hook {self.hook} priority {self.priority}; policy accept;\n'
        for rule in self.rules:
            content += f'       {inbound_interfaces} {rule}\n'
        content += f'    }}\n'
        content += f'}}\n'
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
        self.ip_network = ipaddress.ip_network(ip_prefix)

    def get_ips_count(self) -> int:
        """Returns the number of IPs in a prefix.

        Example:
        % ip = IPOperations('192.0.2.0/30')
        % ip.get_ips_count()
        4
        """
        if '/31' in self.ip_prefix:
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
        """Converts a prefix to a list of IPs including the network and broadcast addresses.

        Example:
        % ip = IPOperations('192.0.2.0/30')
        % ip.convert_prefix_to_list_ips()
        ['192.0.2.0', '192.0.2.1', '192.0.2.2', '192.0.2.3']
        """
        if '/31' in self.ip_prefix:
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


# def convert_port_range_to_int(port_range):
#     start, end = port_range.split('-')
#     return int(start), int(end)
#
#
# def get_next_port_range(port_range, port_count=1024):
#     start, end = convert_port_range_to_int(port_range)
#     return start + port_count, end + port_count


def generate_port_rules(
    external_hosts: list,
    internal_hosts: list,
    port_count: int,
    global_port_range: str = '1024-65535',
) -> list:
    """Generates list of nftables rules for the batch file."""
    rules = []
    start_port, end_port = map(int, global_port_range.split('-'))
    total_possible_ports = (end_port - start_port) + 1

    # Calculate the required number of ports per host
    required_ports_per_host = port_count

    # Check if there are enough external addresses for all internal hosts
    if required_ports_per_host * len(internal_hosts) > total_possible_ports * len(
        external_hosts
    ):
        raise ValueError("Not enough ports available for the specified parameters")

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

        for protocol in ('tcp', 'udp'):
            rule = f'meta l4proto {protocol} ip saddr {internal_host} counter snat to {external_host}:{current_port}-{next_end_port}'
            rules.append(rule)

        rules.append(f'ip saddr {internal_host} counter snat to {external_host}')

        current_port = next_end_port + 1
        if current_port > end_port:
            current_port = start_port
            current_external_index += 1  # Move to the next external host

    return rules


def main():
    nft = NftablesOperations()
    # nft.add_table()
    # nft.add_chain()
    print('---')
    # Change the values to required values
    external_prefix = "192.0.2.0/30"
    internal_prefix = "100.64.0.0/28"
    ports_per_user = 8000
    global_port_range = "1024-65535"
    output_filename = 'cgnat.nft'
    # Not implemented, use ports_per_user
    # tcp_ports = 1024
    # udp_ports = 1024
    #
    external_count = IPOperations(external_prefix).get_ips_count()
    internal_count = IPOperations(internal_prefix).get_ips_count()
    external_hosts = IPOperations(external_prefix).convert_prefix_to_list_ips()
    internal_hosts = IPOperations(internal_prefix).convert_prefix_to_list_ips()

    print('external hosts count:', external_count)
    # print('external hosts list:', external_hosts)
    print('internal hosts count', internal_count)
    # print('internal hosts list', internal_hosts)
    print('global port range:', global_port_range)
    print('ports per host count:', ports_per_user)
    print('---')

    try:
        rules = generate_port_rules(
            external_hosts, internal_hosts, ports_per_user, global_port_range
        )
        for rule in rules:
            nft.add_batch_rule(rule)
        # print(nft.generate_batch_file())
        with open(output_filename, 'w') as file:
            file.write(nft.generate_batch_file())
        print(f'To apply rules use: nft -f {output_filename}\n')
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
