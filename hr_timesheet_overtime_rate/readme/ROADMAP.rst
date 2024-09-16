There is a problem with the way this module handles rates for overtime. If the
rate ever changes, things will start to break.

At time of writing (2024-06-28), the way a rate is computed for a date is by
looking _exclusively_ at the corresponding day of the week. This should be more
robust.

Because ``unit_amount`` is computed from ``hours_worked``, this module is not
compatible with ``hr_timesheet_begin_end``. To make this module subsequently
compatible with ``hr_timesheet_begin_end``, ``hours_worked`` must be computed
from ``time_stop`` and ``time_start``, and ``unit_amount`` must use this
module's computation method instead of ``hr_timesheet_begin_end``'s. The
compatibility layer should go into its own module.

Furthermore, the summary view of timesheet sheets are set read-only in this
module. Because of programming complexities, it is not easy to change this view
to use ``hours_worked`` instead of ``unit_amount``.
