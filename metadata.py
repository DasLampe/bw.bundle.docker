defaults = {
}

if node.has_bundle("apt"):
    defaults['apt'] = {
        'packages': {
            'curl': {'installed': True},
            'ca-certificates': {'installed': True},
        }
    }

if node.has_bundle('iptables'):
    defaults['iptables'] = {
        'policies': {
            'filter': {
                'DOCKER': '-',
                'DOCKER-ISOLATION-STAGE-1': '-',
                'DOCKER-ISOLATION-STAGE-2': '-',
                'DOCKER-USER': '-',
            }
        },
        'rules': [
            repo.libs.iptables.jump('DOCKER-USER').chain('FORWARD').version(4).prio(30),
            repo.libs.iptables.jump('DOCKER-ISOLATION-STAGE-1').chain('FORWARD').version(4).prio(40),

            repo.libs.iptables.accept().chain('FORWARD').version(4).output('docker0')
                .ctstate('RELATED,ESTABLISHED').prio(55),
            repo.libs.iptables.jump('DOCKER').chain('FORWARD').version(4).output('docker0').prio(56),
            repo.libs.iptables.accept().chain('FORWARD').version(4).input('docker0').output('docker0', True).prio(57),
            repo.libs.iptables.accept().chain('FORWARD').version(4).input('docker0').output('docker0').prio(58),

            repo.libs.iptables.jump('DOCKER-ISOLATION-STAGE-2').chain('DOCKER-ISOLATION-STAGE-1')
                .version(4).input('docker0').output('docker0', True).prio(20),

            repo.libs.iptables.jump('RETURN').chain('DOCKER-ISOLATION-STAGE-1').version(4).prio(9999),

            repo.libs.iptables.jump('DROP').chain('DOCKER-ISOLATION-STAGE-2').version(4).output('docker0').prio(5000),
            repo.libs.iptables.jump('RETURN').chain('DOCKER-ISOLATION-STAGE-2').version(4).prio(9999),

            repo.libs.iptables.jump('RETURN').chain('DOCKER-USER').version(4).prio(9999),
        ]
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


@metadata_reactor
def ignore_iptables_chains(metadata):
    if not node.has_bundle('iptables'):
        raise DoNotRunAgain

    rules = []
    prio = 100
    for bridge in sorted(metadata.get('docker/additional_bridges', [])):
        rules += [
            repo.libs.iptables.accept().chain('FORWARD').version(4).output(bridge).ctstate('RELATED,ESTABLISHED')
                .prio(prio),
            repo.libs.iptables.jump('DOCKER').chain('FORWARD').version(4).output(bridge).prio(prio + 1),
            repo.libs.iptables.accept().chain('FORWARD').version(4).input(bridge).output(bridge, True).prio(prio + 2),
            repo.libs.iptables.accept().chain('FORWARD').version(4).input(bridge).output(bridge).prio(prio + 3),

            repo.libs.iptables.jump('DOCKER-ISOLATION-STAGE-2').chain('DOCKER-ISOLATION-STAGE-1').version(4)
                .input(bridge).output(bridge, True).prio(prio + 5000),

            repo.libs.iptables.jump('DROP').chain('DOCKER-ISOLATION-STAGE-2').version(4).output(bridge)
                .prio(prio + 5000),
        ]

        prio += 10

    return {
        'iptables': {
            'rules': rules,
        }
    }
