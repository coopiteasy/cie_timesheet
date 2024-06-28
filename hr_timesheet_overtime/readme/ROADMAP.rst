There is a problem with the way this module handles rates for overtime. If the
rate ever changes, things will start to break.

At time of writing (2024-06-28), the way a rate is computed for a date is by
looking _exclusively_ at the corresponding day of the week. This should be more
robust.

Furthermore, when inserting hours worked, the actual hours worked get lost. You
(try to) write a value to ``unit_amount``, but an augmented value gets written
to the field instead. This is rather ugly.

We can improve this by relying on the computation of ``unit_amount`` in Odoo
≥16: create a new field ``hours_worked``, which contains the actual hours worked
sans rate. Then, compute ``unit_amount`` from ``hours_worked`` (in a more robust
fashion than is presently the case). In the interface, show ``hours_worked``
more prominently than ``unit_amount`` as the main editable field.

To make this module subsequently compatible with ``hr_timesheet_begin_end``,
``hours_worked`` must be computed from ``time_stop`` and ``time_start``, and
``unit_amount`` must use this module's computation method instead of
``hr_timesheet_begin_end``'s. The compatibility layer should go into its own
module.
