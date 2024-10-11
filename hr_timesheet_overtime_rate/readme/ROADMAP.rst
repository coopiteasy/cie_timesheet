There is a problem with the way this module handles rates for overtime. If the
rate ever changes, things will start to break.

At time of writing (2024-06-28), the way a rate is computed for a date is by
looking _exclusively_ at the corresponding day of the week. This should be more
robust.

Furthermore, the summary view of timesheet sheets are set read-only in this
module. Because of programming complexities, it is not easy to change this view
to use ``hours_worked`` instead of ``unit_amount``.
