import xml.etree.ElementTree as ET
import uuid
import os


from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        hosts=dict(type='list', required=True),
        group_name=dict(type='str', required=True),
        users_file=dict(type='str', required=True),
        authorizations_file=dict(type='str', required=True)
    )

    module = AnsibleModule(argument_spec=module_args)
    new_group_name = module.params['group_name']
    users_file = module.params['users_file']
    authorizations_file = module.params['authorizations_file']
    hosts = module.params['hosts']
    changed_status=False
    # new_group_identifier = str(uuid.uuid4())
    new_group_identifier = "1fe2870d-1e9a-4585-bd27-5e1ad2ca411d" # str(uuid.uuid4())
    new_group_resources = {
        "/proxy": "W",
        "/controller": "R"
    }

    result = {
        "users_updated": False,
        "authorizations_updated": False
    }

    if os.path.exists(users_file) and os.path.exists(authorizations_file):
        try:
            users = ET.parse(users_file)
            tenants = users.getroot()
            if tenants.tag == "tenants":
                # users_section = tenants.find("users")
                groups_section = tenants.find("groups")
                new_group_element = groups_section.find(f"group[@name='{new_group_name}']")
                if new_group_element is not None:
                    new_group_identifier = new_group_element.get("identifier")
                    new_group_element.clear()
                    new_group_element.set("identifier", new_group_identifier)
                    new_group_element.set("name", new_group_name)
                    result["users_updated"] = True
                else:
                    new_group_element = ET.Element("group", identifier=new_group_identifier, name=new_group_name)
                    groups_section.append(new_group_element)
                    result["users_updated"] = True
                for host in hosts:
                    users_section = tenants.find("users")
                    host_identifier = str(uuid.uuid4())
                    existing_users_names = {user.get("identity"): user.get("identifier") for user in
                                            users_section.findall("user")}
                    if host not in existing_users_names:
                        new_user_element = ET.Element("user", identifier=host_identifier, identity=host)
                        users_section.append(new_user_element)
                        result["users_updated"] = True
                    else:
                        host_identifier = existing_users_names[host]
                    new_host_element = ET.Element("user", identifier=host_identifier)
                    new_group_element.append(new_host_element)

            authorizations = ET.parse(authorizations_file)
            root = authorizations.getroot()

            if root.tag == "authorizations":
                policies_section = root.find("policies")
                for resource_to_find, action_to_find in new_group_resources.items():
                    policy = policies_section.find(f"policy[@resource='{resource_to_find}'][@action='{action_to_find}']")
                    if policy is not None:
                        existing_groups = {group.get("identifier") for group in policy.findall("group")}
                        if new_group_identifier not in existing_groups:
                            new_group_element = ET.Element("group", identifier=new_group_identifier)
                            policy.append(new_group_element)
                            result["authorizations_updated"]=True

            if result["users_updated"]:
                users.write(users_file, encoding="utf-8", xml_declaration=True)

            # if result["authorizations_updated"]:
                # authorizations.write(authorizations_file, encoding="utf-8", xml_declaration=True)

            changed_status = result["users_updated"] | result["authorizations_updated"]
            module.exit_json(changed=changed_status, **result)
        except Exception as e:
            module.fail_json(msg=str(e))
    module.exit_json(changed=changed_status, **result)


if __name__ == '__main__':
    run_module()