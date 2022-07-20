#!/usr/bin/env python3
# coding=utf-8

# SPDX-FileCopyrightText: © 2022 David Parsons
# SPDX-License-Identifier: MIT
import base64
from collections import OrderedDict
import dictdiffer
import hashlib
import os.path
import sys
import vmx


if sys.version_info < (3, 10):
    sys.stderr.write('You need Python 3.10 or later\n')
    sys.exit(1)


def printdiff(dict1, dict2):
    diffs = dictdiffer.diff(dict1, dict2, expand=True)
    for diff in list(diffs):
        if diff[1] == [0]:
            print(f'Diff {diff[2][1]}->{diff[2][0]}')
        else:
            print(diff)


def vmxdirect():
    pref = vmx.VMX('/Users/dave/Library/Preferences/VMware Fusion/preferences')

    # !!These are only for my MacBook Pro!!
    def_profile_std = '52dedf7b-bfa1-9fb1-54bc-756dc84edff3'
    def_profile_mac = '52420d3d-817e-6c3b-2983-196d98e08339'

    pref_defaultProfileKey = pref['pref.keyboardAndMouse.defaultProfileKey']
    pref_vmHotKey_count = pref['pref.keyboardAndMouse.vmHotKey.count']
    pref_vmHotKey_enabled = pref['pref.keyboardAndMouse.vmHotKey.enabled']
    pref_maxProfiles = int(pref['pref.keyboardAndMouse.maxProfiles'])

    profiles = OrderedDict()
    for i in range(0, pref_maxProfiles):
        prof_profileName = pref[f'pref.keyboardAndMouse.profile{i}.profileName']
        prof_profileType = pref[f'pref.keyboardAndMouse.profile{i}.profileType']
        prof_profileKey = pref[f'pref.keyboardAndMouse.profile{i}.profileKey']
        prof_cmdKeyFilterType = pref[f'pref.keyboardAndMouse.profile{i}.cmdKeyFilterType']
        prof_enableKeyMappings = pref[f'pref.keyboardAndMouse.profile{i}.enableKeyMappings']
        prof_enableOSShortcuts = pref[f'pref.keyboardAndMouse.profile{i}.enableOSShortcuts']
        prof_languageSpecificKeyMappingsEnabled = pref[f'pref.keyboardAndMouse.profile{i}.languageSpecificKeyMappingsEnabled']
        prof_selectedLanguage = pref[f'pref.keyboardAndMouse.profile{i}.selectedLanguage']
        prof_maxMappings = int(pref[f'pref.keyboardAndMouse.profile{i}.maxMappings'])
        profiles[prof_profileKey] = [prof_profileName, dict()]
        mapping = profiles[prof_profileKey][1]
        for j in range(0, prof_maxMappings):
            map_mappingKey = pref[f'pref.keyboardAndMouse.profile{i}.mapping{j}.mappingKey']
            map_fromHost = pref[f'pref.keyboardAndMouse.profile{i}.mapping{j}.fromHost']
            map_toGuest = pref[f'pref.keyboardAndMouse.profile{i}.mapping{j}.toGuest']
            map_enabled = pref[f'pref.keyboardAndMouse.profile{i}.mapping{j}.enabled']
            mapping[map_fromHost] = [map_fromHost, map_toGuest, map_enabled]
            # print(f'Key: {map_mappingKey} Host: {map_fromHost} Guest: {map_toGuest} Enabled: {map_enabled}')

    print('Keyboard Layout Details')
    print('-----------------------\n')
    print(f'# of Profiles:      {pref_maxProfiles}\n')
    print(f'Fusion std profile: {def_profile_std}')
    print(f'Fusion mac profile: {def_profile_mac}')
    print(f'Default Profile:    {pref_defaultProfileKey}\n')
    print(f'HotKey Enabled:     {pref_vmHotKey_enabled}')
    print(f'HotKey Count:       {pref_vmHotKey_count}\n')

    for i in range(0, pref_maxProfiles):
        prof_profileName = pref[f'pref.keyboardAndMouse.profile{i}.profileName']
        prof_profileKey = pref[f'pref.keyboardAndMouse.profile{i}.profileKey']
        prof_profileType = pref[f'pref.keyboardAndMouse.profile{i}.profileType']
        if prof_profileKey != pref_defaultProfileKey and prof_profileKey != def_profile_mac:
            print(f'Name: {prof_profileName} Type: {prof_profileType} Key: {prof_profileKey}')
            printdiff(profiles[pref['pref.keyboardAndMouse.defaultProfileKey']], profiles[prof_profileKey])
            print('\n')
    return


if __name__ == '__main__':
    vmxdirect()
    pass
