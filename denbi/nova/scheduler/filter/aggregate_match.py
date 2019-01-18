from oslo_log import log as logging


from nova.scheduler import filters
from nova.scheduler.filters import extra_specs_ops
from nova.scheduler.filters import utils


LOG = logging.getLogger(__name__)

_SCOPE = 'aggregate_match'


class AggregateMatchFilter(filters.BaseHostFilter):
    """AggregateMatchFilter requires a match between host and instance specs."""

    # Aggregate data and instance type does not change within a request
    run_filter_once_per_request = True

    RUN_ON_REBUILD = False

    def host_passes(self, host_state, spec_obj):
        """Return whether the instance matches the host's spec. All host's
        metadata entries have to be present. It effectively filters out
        flavors and images without the required or even no specs.
  	"""

        # get the host/aggregate specs
        metadata = utils.aggregate_metadata_get_by_host(host_state)

        # try to get the instance specs
        instance_type = spec_obj.flavor

        # If 'extra_specs' is not present or extra_specs are empty then we
        # need not proceed further
        if (not instance_type.obj_attr_is_set('extra_specs')
                or not instance_type.extra_specs):
            # if no instance specs are present, the host is denied if it defines
            # some specs
            return not metadata

        for key, req in metadata.items():
            aggregate_vals = instance_type.extra_specs.get(key, None)
            if not aggregate_vals:
                # keys may be scoped with 'aggregate_instance_extra_specs'
                aggregate_vals = instance_type.extra_specs.get("aggregate_instance_extra_specs:"+key, None)
		if not aggregate_vals:
                    LOG.debug("%(extra_specs)s fails require host extra_specs, key %(key)s is not in instance definition.",
                               {'extra_specs': instance_type.extra_specs, 'key': key})
                return False
            for aggregate_val in aggregate_vals:
                if not extra_specs_ops.match(aggregate_val, req):
                    LOG.debug("%(extra_specs)s fails required host extra_specs, '%(aggregate_vals)s' do not "
                              "match '%(req)s' for key %{key}s.",
                              {'extra_specs': instance_type.extra_specs, 'req': req,
                               'aggregate_vals': aggregate_vals, 'key': key})
                return False
        return True
