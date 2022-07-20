#!/usr/bin/env python3
# coding=utf-8

# SPDX-FileCopyrightText: © 2022 David Parsons
# SPDX-License-Identifier: MIT

import base64
import hashlib
import os.path
import sys
import vmx

ROOT = 'ROOT'
VM = 'VM'
VM_ID = -1
VM_NAME = 'Virtual Machines'
SVM = 'SVM'
SVM_ID = -2
SVM_NAME = 'Shared Virtual Machines'

if sys.version_info < (3, 10):
    sys.stderr.write('You need Python 3.10 or later\n')
    sys.exit(1)


def create_vmid(filename):
    sha1 = hashlib.sha1(filename.encode()).digest()
    return base64.b32hexencode(sha1).decode('utf-8')


def print_tree(inventory, hierarchy):
    for node in inventory:
        # if node[0] == ROOT:
        #     parentid = VM_NAME
        # else:
        #     parentid = hierarchy[node[0]]['displayname']
        childid = hierarchy[node[1]]['displayname']
        depth = node[3]
        state = hierarchy[node[1]]['state']
        if state == 'folder':
            state = '📁'
        elif state == 'normal':
            state = '👍'
        elif state == 'broken':
            state = '👎'
        # print(f'parent: {parentid} child: {childid} seq: {seqid} depth: {depth}')
        print(f'{" "*(depth+1)}{childid} [{node[1]}] {state}')
    return

def build_hierarchy(vms, hierarchy, conf2vmid, nodeid2vmid, roots):

    # First pass get config, nodeid and vmid
    for key, value in vms.items():
        # print(key, value)
        key = key.lower()
        if key[0:6] == 'vmlist' and '.config' in key and value != '':
            nodeid = int(key.replace('vmlist', '').replace('.config', ''))
            vmid = create_vmid(value)
            hierarchy[vmid] = dict(config=value, nodeid=nodeid)
            conf2vmid[value] = vmid
            nodeid2vmid[nodeid] = vmid

    # Second pass process subset for additonal details and find root nodes
    for key, value in hierarchy.items():

        # print(key, value)
        key_prefix = f'vmlist{value["nodeid"]}'

        parent_nodeid = vms.as_int(f'{key_prefix}.parentid')
        seqid = vms[f'{key_prefix}.seqid']

        if parent_nodeid == 0:
            roots.append([ROOT, key, seqid, 0])
            hierarchy[key]['parentid'] = ROOT
        else:
            hierarchy[key]['parentid'] = nodeid2vmid[parent_nodeid]

        hierarchy[key]['seqid'] = seqid
        hierarchy[key]['displayname'] = vms[f'{key_prefix}.displayname']
        if 'folder' not in hierarchy[key]['config']:
            hierarchy[key]['state'] = vms[f'{key_prefix}.state']
        else:
            hierarchy[key]['state'] = 'folder'

    # Sort the roots by seqid
    roots.sort(key=lambda y: y[2])
    return


def recurse(tree, hierarchy, node, depth=0):
    tree.append(node)
    children = list()
    for key, value in hierarchy.items():
        parentid = value['parentid']
        seqid = value['seqid']
        if parentid == node[1]:
            children.append([node[1], key, seqid, depth + 1])

    children.sort(key=lambda y: y[2])
    for child in children:
        recurse(tree, hierarchy, child, depth + 1)

    return


def get_inventory():
    user_path = os.path.expanduser('~/Library/Application Support/VMware Fusion/vmInventory')
    user_inventory = vmx.VMX(user_path)
    user_hierarchy = dict()
    user_conf2vmid = dict()
    user_nodeid2vmid = dict()
    user_roots = list()
    build_hierarchy(user_inventory, user_hierarchy, user_conf2vmid, user_nodeid2vmid, user_roots)
    del user_inventory

    shared_path = '/Library/Application Support/VMware/VMware Fusion/Shared/vmInventory'
    shared_inventory = vmx.VMX(shared_path)
    shared_hierarchy = dict()
    shared_conf2vmid = dict()
    shared_nodeid2vmid = dict()
    shared_roots = list()
    build_hierarchy(shared_inventory, shared_hierarchy, shared_conf2vmid, shared_nodeid2vmid, shared_roots)
    del shared_inventory

    user_inventory = list()
    for root in user_roots:
        recurse(user_inventory, user_hierarchy, root)
    print(VM_NAME)
    print_tree(user_inventory, user_hierarchy)

    shared_inventory = list()
    for root in shared_roots:
        recurse(shared_inventory, shared_hierarchy, root)
    print(SVM_NAME)
    print_tree(shared_inventory, shared_hierarchy)

    return


if __name__ == '__main__':
    get_inventory()
    pass
