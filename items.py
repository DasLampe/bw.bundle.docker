COMPOSE_VER = node.metadata.get('docker', {}).get('compose_version', '1.27.4')

composer_check_sums = {
    '1.24.0': 'bee6460f96339d5d978bb63d17943f773e1a140242dfa6c941d5e020a302c91b',
    '1.27.4': '04216d65ce0cd3c27223eab035abfeb20a8bef20259398e3b9d9aa8de633286d',
}

pkg_apt = {
    'docker-ce': {
        'needs': [
            'action:docker_install_apt_key',
            'file:/etc/apt/sources.list.d/docker-ce.list'
        ]
    },
    'docker-compose': {
        'installed': False
    }
}

svc_systemd = {
    'docker': {
      'running': True,
      'needs': ['pkg_apt:docker-ce']
    }
}

files = {
    '/etc/apt/sources.list.d/docker-ce.list': {
      'owner': 'root',
      'group': 'root',
      'mode': '0444',
      'needs': ['action:docker_install_apt_key'],
      'triggers': ['action:update_apt_cache']
    }
}

# TODO: move this to Keychain file
actions = {
    'docker_install_apt_key': {
        'command': 'curl -L https://download.docker.com/linux/debian/gpg | apt-key add -',
        'needs': ['pkg_apt:curl'],
        'unless': 'apt-key list | grep "Docker Release (CE deb) <docker@docker.com>"'
    },
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
