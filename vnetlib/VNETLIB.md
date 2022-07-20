# VMWare Networking CLI


# macOS

Path: `/Applications/VMWare Fusion/Contents/Library/vmnet-cfgcli`

## vnetlib sub-commands

## setloglevel

Set the log level. This does not seem to persist. Receives an integer,
with larger value enabling more verbose output. Seems to be `>= 40`
will enable debug output.

```
$ vmnet-cfgcli setloglevel 50
```

## getloglevel

Returns the currently set log level.

```
$ vmnet-cfgcli getloglevel
```

## setdefaultloglevel

Set the default log level. Setting this will persist the log level.
Value `>= 40` will enable debug output.

```
$ vmnet-cfgcli setdefaultloglevel 50
```

## getdefaultloglevel

Returns the currently set default log level.

```
$ vmnet-cfgcli getdefaultloglevel
```

## servicestart

Start a specific vmware networking service. Valid types:

* dhcp
* nat

```
$ vmnet-cfgcli servicestart vmnet8 nat
```

## servicestop

Stop a specific vmware networking service. Valid types:

* dhcp
* nat

```
$ vmnet-cfgcli servicestop vmnet8 nat
```

## servicestatus Valid types:

* dhcp
* nat

Check status of a specific vmware networking service.

```
$ vmnet-cfgcli servicestatus vmnet8 nat
```

# Networking information/configuration

## getvmnetfeatures

Returns list of configured features and runtime features for
a given devices.

```
$ vmnet-cfgcli getvmnetfeatures vmnet8
```

## gethostadapterlist

Returns list of the adapters currently enabled on the host.

```
$ vmnet-cfgcli gethostadapterlist
```

## getbridge

Returns host adapter bridged to the given virtual adapter.

```
$ vmnet-cfgcli getbridge vmnet8
```

## movebridge

Unknown

```
$ vmnet-cfgcli movebridge ?
```

## getdhcpusage

Returns if DHCP is configured to be used on the given device.

```
$ vmnet-cfgcli getdhcpsuage vmnet8
```

## setdhcpusage

Enable/disable DHCP on a given device

```
$ vmnet-cfgcli setdhcpusage vmnet8 yes # enable
$ vmnet-cfgcli setdhcpusage vmnet8 no  # disable
```

## updatedhcpfromconfig

Updates dhcpd.conf file for the given device based on settings
in the networking file. The DHCP service must be stopped for
the update to be applied, otherwise it will fail.

```
$ vmnet-cfgcli updatedhcpfromconfig vmnet8
```

## getdhcpparam

Unknown. Cannot determine correct param names.
leasebeginip
leaseendip
defleasetime
maxleasetim

```
$ vmnet-cfgcli getdhcpparam vmnet8 PARAM
```

## setdhcpparam

Unknown. Cannot determine correct param names.
leasebeginip
leaseendip
defleasetime
maxleasetim

```
$ vmnet-cfgcli setdhcpparam vmnet8 PARAM VALUE
```

## setdhcpmac2ip

Reserve an IP for a specific MAC on given device.

```
$ vmnet-cfgcli setdhcpmac2ip vmnet8 00:50:56:2B:1C:A3 172.16.30.129
```

## getdhcpmac2ip

Returns IP address reserved for specific MAC on given device. It
is important to note this is _not_ used for discovery of active IP address
lease for a MAC.

```
$ vmnet-cfgcli getdhcpmac2ip vmnet8 00:50:56:2B:1C:A3
```

## enumdhcpmac2ip

Returns all reserved MAC/IP mappings on given device.

```
$ vmnet-cfgcli enumdhcpmac2ip vmnet8
```

## getnatusage

Returns if NAT is enabled on given device.

```
$ vmnet-cfgcli getnatusage vmnet8
```

## setnatusage

Enable/disable NAT on given device

```
$ vmnet-cfgcli setnatusage vmnet8 yes # enable
$ vmnet-cfgcli setnatusage vmnet8 no  # disable
```

## updatenatfromconfig

Update NAT configuration for given device using configuration defined
within the networking file.

```
$ vmnet-cfgcli updatenatfromconfig vmnet8
```

## getnatparam

Unknown. Cannot determine correct parameter names.

gateway
port
activeftp
allowoui
udptimeout

```
$ vmnet-cfgcli getnatparam vmnet8 PARAM
```

## setnatparam

Unknown. Cannot determine correct parameter names.

gateway
port
activeftp
allowoui
udptimeout

```
$ vmnet-cfgcli setnatparam vmnet8 PARAM VALUE
```

## getnatportfwd

Get the Guest IP and port for a current port forward using the
provided device, protocol, and host port.

```
$ vmnet-cfgcli getnatportfwd vmnet8 tcp 8080
```

## setnatportfwd

Add a new port forward on the given device. Parameter structure:
`DEVICE PROTOCOL HOST_PORT GUEST_IP GUEST_PORT`

_NOTE: Description cannot be set with the CLI command_

```
$ vmnet-cfgcli setnatportfwd vmnet8 tcp 8080 172.16.30.129 80
```

This can also be used to remove a port forward by only specifying the
`DEVICE PROTCOL HOST_PORT`

```
$ vmnet-cfgcli setnatportfwd vmnet8 tcp 8080
```

## enumportfwd

Return list of port forwards for given device.

```
$ vmnet-cfgcli enumportfwd vmnet8
```

## deletevnet

Deletes device configuration from networking file

```
$ vmnet-cfgcli deletevnet vmnet8
```

## disablehostonlyadap

Disable a host only adapter. This will disable the given adapter
but does not remove it.

_NOTE: Exit code is always `1`_

```
$ vmnet-cfgcli disablehostonlyadap vmnet8
```

## enablehostonlyadap

Enable a currently disabled host only adapter.

```
$ vmnet-cfgcli enablehostonlyadap vmnet8
```

## updateadapterfromconfig

Updates the given adapter from the networking configuration file.

_NOTE: Exit code is always `1`_

```
$ vmnet-cfgcli updateadapterfromconfig vmnet8
```

## assignsubnet

Returns the subnet currently assigned to the given device.

```
$ vmnet-cfgcli assignsubnet vmnet8
```

## addadapter

Create a new virtual device. Automatically assigns a new subnet.

_NOTE: Even devices get `172.16.x.x` addresses, odd get `192.168.x.x`_

```
$ vmnet-cfgcli addadapter vmnet4
```

## removeadapter

Remove a virtual device.

```
$ vmnet-cfgcli removeadapter vmnet4
```

## getvmnetcount

Provides number of configured vmnets.

_NOTE: This currently just returns count of `256` and reports an error._

```
$ vmnet-cfgcli getvmnetcount
```

## getvnetwithfeatures

Unknown. This looks to be a tool to query existing adapters that match
a specific query. Unknown what query structure looks like.

```
$ vmnet-cfgcli getvnetwithfeatures QUERY
```

## setsubnetaddr

Set the subnet address on a device. Can be used when adding a new interface
to adjust assigned address prior to creating the actual device.

```
$ vmnet-cfgcli setsubnetaddr vmnet8 192.168.33.1
```

## setsubnetmask

Set the subnet mask on the device. Can be used when adding a new interface
to adjust the assigned subnet mask prior to creating the actual device.

```
$ vmnet-cfgcli setsubnetmask vment8 255.255.255.0
```

## vnetcfgget

Get a configuration value that was set on an adapter. These are freeform
configuration values, not values that are used internally(?).

```
$ vmnet-cfgcli vnetcfgget vmnet8 mykey
```

## vnetcfgadd

Add a new configuration value to an adapter. These are freeform
configuration values, not values that are used internally(?).

```
$ vmnet-cfgcli vnetcfgadd vmnet8 mykey:myvalue
```

## vnetcfgremove

Remove a configuration key from an adapter.

```
$ vmnet-cfgcli vnetcfgremove vmnet8 mykey
```

## getdefaultbridge

Returns the default interface used for bridging. The value returned
is the `vmnet` number, which can be tracked to a physical device
name using the `gethostadapterlist` command.

```
$ vmnet-cfgcli getdefaultbridge
```

## setdefaultbridge

Set the default interface used for bridging to the given value. Value
should be the `vmnet` number of the interface, which can be found
using the `gethostadapterlist` command.

```
$ vmnet-cfgcli setdefaultbridge 0
```

## exportconfig

Export the current networking configuration to the given path.

```
$ vmnet-cfgcli exportconfig /path/to/networking.config
```

## importconfig

Import networking configuration from the given path.

```
$ vmnet-cfgcli importconfig /path/to/networking.config
```

## createdb

Creates and initializes the networking configuration database (the `networking` file).

_NOTE: This will remove an existing `networking` file and all of it's contents._

```
$ vmnet-cfgcli createdb
```

## getunusedsubnet

Returns a valid subnet and mask that is currently unused.

```
$ vmnet-cfgcli getunusedsubnet
```

## getunusedvnet

Returns a valid unused vmnet name (like `vmnet4`).

_NOTE: This uses `getvnetwithfeatures` library internally and is likely useful
in figuring out query syntax at some point._

```
$ vmnet-cfgcli getunusedvnet
```
