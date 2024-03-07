#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    path:
        description: This is the path for txt dicument
        required: true
        type: str
    content:
        description: This is text for txt document
        required: true
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Evgeniy Os (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.test_module:
    path: /test
    content 'test'
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from pathlib import Path
from ansible.module_utils.basic import AnsibleModule

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        content=dict(type='str', required=True),
        path=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        failed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)
    
    def write_to_file():
        my_file = open(module.params['path'], "w")
        my_file.write(module.params['content'])
        my_file.close()

    my_file = Path(module.params['path'])

    try:
        my_abs_path = my_file.resolve(strict=True)
    except FileNotFoundError:
        write_to_file()
        result = dict(changed=True, failed=False, message = '{} - text was written to file!'.format(module.params['content']))
    else:
        my_file = open(module.params['path'], "r")
        if my_file.read() == module.params['content']:
            result = dict(changed=False, failed=False)
        else:
            write_to_file()
            result = dict(changed=True, failed=False, message = '{} - text was written to file!'.format(module.params['content']))

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
