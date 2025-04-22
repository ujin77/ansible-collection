#!/usr/bin/python
# -*- coding: utf-8 -*-

# modules/password_hash.py
from passlib.hash import sha512_crypt


from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        password=dict(type='str', required=True),
    )

    module = AnsibleModule(argument_spec=module_args)
    try:

        password = module.params['password']
        hashed_password = sha512_crypt.hash(password, rounds=5000)  # 5000 (Linux default)
        result = {
            'hash': hashed_password
        }
        module.exit_json(changed=True, **result)
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    run_module()