from datetime import date, timedelta

from parsy import fail, generate, regex, seq, string


class ISO8601Parser:
    @classmethod
    def parse(cls, input):
        ### Date Method 1
        # year = regex(r"[0-9]{4}").map(int).desc("4 digit year")
        # month = regex("[0-9]{2}").map(int).desc("2 digit month")
        # day = regex(r"[0-9]{2}").map(int).desc("2 digit day")
        # dash = string("-")
        # full_date = seq(year=year << dash, month=month << dash, day=day).combine_dict(date)
        # output = full_date.parse(input)

        ### Date Method 2
        # output = cls._parse_full_or_partial_date.parse(input)

        ### Days Ago
        days_ago = regex(r"[0-9]+").map(lambda d: timedelta(days=-int(d))) << string(" days ago")

        ### Flexible Date
        flexi_date = cls._parse_full_or_partial_date | days_ago
        output = flexi_date.parse(input)

        print(output)

    @generate
    @staticmethod
    def _parse_full_or_partial_date():
        y = None
        m = None
        d = None
        year = regex(r"[0-9]{4}").map(int).desc("4 digit year")
        month = regex("[0-9]{2}").map(int).desc("2 digit month")
        day = regex(r"[0-9]{2}").map(int).desc("2 digit day")
        optional_dash = string("-").optional()
        y = yield year
        dash1 = yield optional_dash
        if dash1 is not None:
            m = yield month
            dash2 = yield optional_dash
            if dash2 is not None:
                d = yield day
        if m is not None:
            if m < 1 or m > 12:
                return fail("month must be in 1..12")
        if d is not None:
            try:
                date(y, m, d)
            except ValueError as e:
                return fail(e.args[0])
        return (y, m, d)


if __name__ == "__main__":
    full_date_input = "2024-03-14"
    ISO8601Parser.parse(full_date_input)

    partial_date_input = "2000-01"
    ISO8601Parser.parse(partial_date_input)

    # expected to fail, since it isn't a leap year
    # invalid_date_input = "2017-02-29"
    # ISO8601Parser.parse_date(invalid_date_input)

    days_ago_input = "5 days ago"
    ISO8601Parser.parse(days_ago_input)

    # expected to fail, invalid date format
    # invalid_date_format = "2021-"
    # ISO8601Parser.parse(invalid_date_format)

    # expected to fail, invalid "days ago" format
    # invalid_days_ago_format = "2 years ago"
    # ISO8601Parser.parse(invalid_days_ago_format)
