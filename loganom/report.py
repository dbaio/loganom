"""Class to store/generate reports

Two types of output.

Single value (email/value):

+------------------------------------------+------+
| user@domain                              | 781  |
| userb@domain                             | 409  |
| userc@domainc                            | 409  |
+------------------------------------------+------+

Multiple values (email/value[s]):

+------------------------------------------------------------------------------+
|                                  user@domain                                 |
+==============================================================================+
| RS - Belgrade - unknown - AS31042 Serbia BroadBand-Srpske Kablovske mreze    |
| LT - Vilnius - md-Y-X-195-171.omni.lt. - AS8764 Telia Lietuva, AB            |
| BA - Bihać - unknown - AS9146 BH Telecom d.d. Sarajevo                       |
+------------------------------------------------------------------------------+
"""

from texttable import Texttable

# pylint: disable=R0903
class Report():
    """Class to store/generate reports."""

    def __init__(self, table_type, data):
        """Initialize Report Class

        Args:
            table_type (string): single/multi
            data (defaultdict(list)): defaultdict['email'] --> list_values
        """
        self.table_type = table_type
        self.data = data


    def generate_table(self, border=True, short=True):
        """Generate a Textable string with the report.

        Args:
            border (bool, optional): Border around the table. Defaults to True.
            short (bool, optional): Return only 10 rows/values. Defaults to False.
            Only for multi tables.
        """

        table_final = ""
        table_obj = Texttable()
        table_obj.set_max_width(80)
        table_count = 0

        for key in self.data.keys():

            if table_count > 0 and self.table_type == 'multi':
                table_final += "\n\n"

            if self.table_type == 'single':
                data_value = self.data[key]
                table_obj.add_row([key, data_value])
            else:
                # Second round, initialize another instance
                if table_count > 0:
                    table_obj = Texttable()
                    table_obj.set_max_width(80)

                table_obj.header([key])

                value_count = 0
                for value in self.data[key]:
                    if short is True and value_count >= 10:
                        table_obj.add_row(['[...]'])
                        break
                    # Print just 80 chars, improve readability
                    short_value = value[0:76]
                    table_obj.add_row([short_value])
                    value_count += 1

            if border is False:
                table_obj.set_deco(Texttable.HEADER | Texttable.VLINES)
            else:
                table_obj.set_deco(Texttable.BORDER | Texttable.HEADER | Texttable.VLINES)

            # Print many tables for multi type
            if self.table_type == 'multi':
                table_final += table_obj.draw()

            table_count += 1

        # Print just one table for single type
        if self.table_type == 'single':
            table_final += table_obj.draw()

        # short=False
        return table_final
