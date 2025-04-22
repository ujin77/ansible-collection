# modules/test.py
from ansible.module_utils.basic import AnsibleModule
import json

def run_module():
    module_args = dict(
        msg=dict(type='str', required=True),
    )
    module = AnsibleModule(argument_spec=module_args)
    result = {
        'msg': module.params['msg'],
        'test': 'OK',
        'status': 'success'
    }
    module.exit_json(changed=False, **result)

if __name__ == '__main__':
    run_module()