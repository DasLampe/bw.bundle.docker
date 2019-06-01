COMPOSE_VER = '1.24.0'
COMPOSE_SUM = 'bee6460f96339d5d978bb63d17943f773e1a140242dfa6c941d5e020a302c91b'

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

svc_systemv = {
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

actions = {
    'docker_install_apt_key': {
        'command': 'curl -L https://download.docker.com/linux/debian/gpg | apt-key add -',
        'needs': ['pkg_apt:curl'],
        'unless': 'apt-key list | grep "Docker Release (CE deb) <docker@docker.com>"'
    },
    'make_executable': {
        'command': 'chmod +x /usr/local/bin/docker-compose',
        'triggered': True,
    }
}

downloads = {
    '/usr/local/bin/docker-compose': {
        'url': 'https://github.com/docker/compose/releases/download/{version}/docker-compose-Linux-x86_64'.format(
            version=COMPOSE_VER,
        ),
        'sha256': COMPOSE_SUM,
        'needs': ['pkg_apt:ca-certificates'],
        'triggers': ['action:make_executable'],
    }
}
