# modules/nifi_user_password.py
# import passlib
from passlib.hash import bcrypt

from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        password=dict(type='str', required=True),
    )

    module = AnsibleModule(argument_spec=module_args)
    try:

        password = module.params['password']
        hashed_password = bcrypt.hash(password)
        result = {
            # 'passlib_version': passlib.__version__,
            'hashed_password': hashed_password
        }
        module.exit_json(changed=True, **result)
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    run_module()