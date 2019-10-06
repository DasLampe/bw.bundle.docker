@metadata_processor
def add_apt_packages(metadata):
    if node.has_bundle("apt"):
        metadata.setdefault('apt', {})
        metadata['apt'].setdefault('packages', {})

        metadata['apt']['packages']['curl'] = {'installed': True}
        metadata['apt']['packages']['ca-certificates'] = {'installed': True}

    return metadata, DONE


@metadata_processor
def add_sudo_group_processor(metadata):
    if 'users' in metadata:
        for username in metadata['users'].keys():
            if metadata['users'][username].get('docker', False):
                add_groups = metadata['users'][username].get('add_groups', [])

                if 'docker' not in add_groups:
                    add_groups.append('docker')

                metadata['users'][username]['add_groups'] = add_groups

        return metadata, DONE

    return metadata, RUN_ME_AGAIN
