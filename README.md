# nova-filter-collection

Collection of additional nova scheduler filters developed
in the de.NBI project

## Implemented filters ##

### AggregateMatch (`denbi.nova.scheduler.filter.aggregate_match`) ###

This match reverses the logik of the existing AggregateInstanceExtraSpecs filter. All specs of a given host/aggregate
have to be present in the instance definition for a host to pass. This allows an easy definition of special duty hosts
that are only available to well defined instances, e.g. GPU hosts. The existing filter does not prevent normal
instances without any extra specs from being scheduled to host or aggregate with certain specs.

Example:

Hosts in the aggregate 'high-mem' should be reserved for instance with high memory requirements. The aggregate is
defined with an extra property:

    (openstack) aggregate show high-mem
    +-------------------+--------------------------------+
    | Field             | Value                          |
    +-------------------+--------------------------------+
    | availability_zone | nova                           |
    ...
    | name              | high-mem                       |
    | properties        | type='high-mem'                |
    ...
    +-------------------+--------------------------------+

A corresponding flavor can be created with

    (openstack) flavor create --property type=high-mem ...... large_ram_flavor

The filter supports either unscoped property, or properties scoped with `aggregate_instance_extra_specs`, e.g.
`aggregate_instance_extra_specs:type=high-mem`. All instances based on flavors without a matching property will
not be scheduled to the high-mem hosts.

Properties can be defined as key-value pairs or use any of the extra spec ops. For more information see https://docs.openstack.org/nova/rocky/user/filter-scheduler.html.

