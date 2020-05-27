#!/usr/bin/python3

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: my_test

short_description: This is my test module

version_added: "2.4"

description:
	- "This is my longer description explaining my test module"

options:
	text:
		description:
		- This is the text to display before or after the login
		required: true
	when:
		description:
		- Is the text to be displayed before of after the login
		required: true
	state:
		description:
		- Should the login message be absent or present
	fqdn:
		description:
		- when true, display an extra line with the fqdn of the system

extends_documentation_fragment:
	- system

author:
	- Fred van Zwieten (@fvzwieten)
'''

EXAMPLES = '''
# make a before login message
- name: Display message before login
  loginmsg:
    text: "Hello, you are entering a Hackathon Machine!”
    when: before
    fqdn: true

# remove an after login message
- name: Remove message after login
  loginmsg:
    text: "Hello, you are entering a Hackathon Machine!”
    when: after
    state: absent

'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule

# needed for fqdn parameter
import socket

# needed for deleting files and writing to files
import os

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        text=dict(type='str', required=True),
        when=dict(type='str', required=True),
        state=dict(type='str', required=False, default="present"),
        fqdn=dict(type=bool, required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    # syntax check on parameter <when> and setup the correct file
    if module.params['when'] == "before":
        file = "/etc/issue"
    elif module.params['when'] == "after":
        file = "/etc/motd"
    else:
        module.fail_json(msg='syntax error in when parameter', **result)

    # extend text with the fqdn, if requested
    if module.params['fqdn']:
        finalmsg = module.params['text'] + "\nServer: " + socket.getfqdn() + "\n"
    else:
        finalmsg = module.params['text'] + "\n"

    # write or delete file based on parameter <state>, including syntax check
    if module.params['state'] == "present":
        if not module.check_mode:
            f = open(file, "w")
            f.write(finalmsg)
            f.close()
        result['changed'] = True
    elif module.params['state'] == "absent":
        if not module.check_mode:
            os.remove(file)
        result['changed'] = True
    else:
        module.fail_json(msg='syntax error in state parameter', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
        
