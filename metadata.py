defaults = {
}

if node.has_bundle("apt"):
    defaults['apt'] = {
        'packages': {
            'curl': {'installed': True},
            'ca-certificates': {'installed': True},
        }
    }


@metadata_reactor
def add_sudo_group_processor(metadata):
    users = {}
    for username in metadata.get('users').keys():
        if metadata.get('users/{}/docker'.format(username), False):
            add_groups = metadata.get('users/{}/add_groups'.format(username), [])

            if 'docker' not in add_groups:
                add_groups.append('docker')

            users[username] = {
                'add_groups': add_groups,
            }

    return {
        'users': users,
    }


# @metadata_processor
# def ignore_iptables_chains(metadata):
#     if node.has_bundle('iptables'):
#         metadata.setdefault('iptables', {})
#         metadata['iptables'].setdefault('ignored', {})
#         metadata['iptables']['ignored'].setdefault('chains', [])
#         metadata['iptables']['ignored'].setdefault('rules', [])
#
#         metadata['iptables']['ignored']['chains'] += [
#             {'table': 'filter', 'chain': 'DOCKER'},
#             {'table': 'filter', 'chain': 'DOCKER-ISOLATION'},
#             {'table': 'filter', 'chain': 'DOCKER-USER'},
#         ]
#
#         metadata['iptables']['ignored']['rules'] += [
#             {'chain': 'FORWARD', 'table': 'filter', 'output': 'docker.*'},
#             {'chain': 'FORWARD', 'table': 'filter', 'input': 'docker.*'},
#             {'chain': 'FORWARD', 'table': 'filter', 'jump': 'DOCKER-ISOLATION'},
#             {'chain': 'FORWARD', 'table': 'filter', 'jump': 'DOCKER-USER'},
#         ]
#
#     return metadata, DONE
