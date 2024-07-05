# SPDX-FileCopyrightText: 2024 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later


def migrate(cr, version):
    # This is not strictly true, but it's the best way to populate the field
    # with sensible data.
    #
    # TODO: Does this run upon module installation? This needs to be run on
    # module installation.
    cr.execute(
        # Perfect symmetry is joyous
        """
        UPDATE account_analytic_line
        SET hours_worked=unit_amount
        WHERE project_id IS NOT NULL
        """
    )
