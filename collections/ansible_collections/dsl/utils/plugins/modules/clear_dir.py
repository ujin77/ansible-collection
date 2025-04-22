#!/usr/bin/python
# -*- coding: utf-8 -*-

# modules/clear_dir.py
from pathlib import Path
import shutil
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
    )
    module = AnsibleModule(argument_spec=module_args)
    changed=False
    result = {
        'path': module.params['path'],
        'status': 'success'
    }
    try:
        dir_path = Path(module.params['path'])
        if dir_path.exists() and dir_path.is_dir() and any(dir_path.iterdir()):
            for item in dir_path.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            changed = True
        else:
            changed = False
            result['status'] = 'Empty'
    except Exception as e:
        module.fail_json(msg=str(e))
    module.exit_json(changed=changed, **result)

if __name__ == '__main__':
    run_module()