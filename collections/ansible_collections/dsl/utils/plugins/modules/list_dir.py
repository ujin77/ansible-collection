#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
from pathlib import Path
from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(argument_spec=dict(
            path=dict(type='str', required=True),
            filename=dict(type='str', required=False),
            exclude=dict(type='str', required=False, default=''),
        )
    )
    changed=False
    result = {
        'list' : [],
        'names' : [],
        # 'add_ext': module.params['add_ext']
        # 'path': module.params['path'],
        # 'status': 'success'
    }
    try:
        dir_path = Path(module.params['path'])
        if dir_path.exists() and dir_path.is_dir() and any(dir_path.iterdir()):
            for item in dir_path.iterdir():
                if item.is_dir():
                    if not re.match(module.params['exclude'], item.name):
                        if module.params['filename']:
                            result['list'].append(f"{module.params['path']}/{item.name}/{module.params['filename']}")
                        else:
                            result['list'].append(f"{module.params['path']}/{item.name}")
                        result['names'].append(f"{item.name}")
                        changed = True
    except Exception as e:
        module.fail_json(msg=str(e))
    module.exit_json(changed=changed, **result)

if __name__ == '__main__':
    main()