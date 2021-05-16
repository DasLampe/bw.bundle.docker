COMPOSE_VER = node.metadata.get('docker', {}).get('compose_version', '1.27.4')

composer_check_sums = {
    '1.24.0': 'bee6460f96339d5d978bb63d17943f773e1a140242dfa6c941d5e020a302c91b',
    '1.27.4': '04216d65ce0cd3c27223eab035abfeb20a8bef20259398e3b9d9aa8de633286d',
}

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
        'docker-compose': {
            'installed': False
        }
    }


symlinks = {
    '/usr/local/bin/docker-compose': {
        'target': f'docker-compose-{COMPOSE_VER}',
        'needs': [f'download:/usr/local/bin/docker-compose-{COMPOSE_VER}', ],
    }
}

downloads = {
    f'/usr/local/bin/docker-compose-{COMPOSE_VER}': {
        'url': f'https://github.com/docker/compose/releases/download/{COMPOSE_VER}/docker-compose-Linux-x86_64',
        'sha256': composer_check_sums[COMPOSE_VER],
        'needs': ['pkg_apt:ca-certificates'],
        'mode': '0755',
    },
}
