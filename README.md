# Docker and docker-compose
This Bundle will install Docker from the docker debian repository

## Requires
This Bundle requires https://github.com/sHorst/bw.bundle.apt to install all required Packages. It also needs the download item which can be found in the bw plugins.
Also it needs metadata with os name and release name, like https://github.com/sHorst/bw.bundle.debian.

## Config
```python
{
    'docker': {
        'compose_version': '1.29.2',
        'daemon_config': {
            'registry-mirrors': [
                'https://<your-mirror>',
            ]
        },
    },
}
```
The `daemon_config` is passed as json into `/etc/docker/daemon.json`.

