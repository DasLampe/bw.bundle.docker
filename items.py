files = {}

if node.has_bundle('apt'):
    files['/etc/apt/sources.list.d/docker-ce.list'] = {
        'content': 'deb [arch=amd64] https://download.docker.com/linux/debian {release_name} stable\n'.format(
            release_name=node.metadata.get(node.os).get('release_name')
        ),
        'content_type': 'text',
        'needs': ['file:/etc/apt/trusted.gpg.d/docker-ce.gpg', ],
        'triggers': ["action:force_update_apt_cache", ],
    }

    files['/etc/apt/trusted.gpg.d/docker-ce.gpg'] = {
        'content_type': 'binary',
    }

    svc_systemd = {
        'docker': {
            'running': True,
            'needs': ['pkg_apt:docker-ce']
        }
    }

    pkg_apt = {
        'docker-ce': {
            'needs': [
                'file:/etc/apt/trusted.gpg.d/docker-ce.gpg',
                'file:/etc/apt/sources.list.d/docker-ce.list'
            ]
        },
    }

if node.metadata.get('docker', {}).get('daemon_config', {}):
    files['/etc/docker/daemon.json'] = {
        'content': json.dumps(node.metadata.get('docker', {}).get('daemon_config', {}), indent=4)
    }