COMPOSE_VER = '1.16.1'
COMPOSE_SUM = 'e2c7c848e1fa388a2e5b8945fdb2660bf8d8adb1'

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
        'unless': 'apt-key list | grep "0EBF CD88"',
        'needs': ['pkg_apt:curl'],
    },
    'download_docker-compose': {
        'command': 'curl -L https://github.com/docker/compose/releases/download/{}/docker-compose-Linux-x86_64 > /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose'.format(COMPOSE_VER),
        'unless': 'sha1sum /usr/local/bin/docker-compose| grep -q ^{}'.format(COMPOSE_SUM),
        'needs': ['pkg_apt:curl'],
    }
}
