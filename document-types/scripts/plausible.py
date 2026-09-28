#!/usr/bin/env python3
"""Make a realistic stand-in for an identifier, for redact.py rules files.

    python document-types/scripts/plausible.py 70-023-651-18 600906626509 PE000008975076479777

An account number replaced with 0000000000 is safe, but it reads as a redaction on a
marketing page: nobody's bill has an account number of all zeros. This returns a value
of the same shape instead. Digits become random digits, while separators, spacing,
letters and length are kept, so the field still looks and parses like the real thing.

Two properties matter more than looking real:

- **Nothing is derived from the original.** A hash or seeded mapping would be
  deterministic, and for a short identifier like a 10-digit account number that can be
  brute-forced back to the original by trying every candidate. Every digit comes from
  `secrets` instead, and no digit keeps its original value in the same position.
- **Reserved ranges where they exist.** US social security numbers use the advertising
  block 987-65-4320 to 987-65-4329, which the SSA never issues, and US phone numbers use
  555-0100 to 555-0199, which are reserved for fiction. Other identifiers (account,
  invoice, meter, order, licence numbers) have no reserved range, but a random value
  beside a fictional name and address identifies no one.

Put the output in the rules file, which stays outside the repo. The same original must
get the same stand-in everywhere it appears, including in other formats: generate once,
then reformat (e.g. with and without spaces) rather than calling this twice.
"""

from __future__ import annotations

import re
import secrets
import sys

SSN = re.compile(r"^\d{3}-\d{2}-\d{4}$")
MASKED_SSN = re.compile(r"^[X*]{3}-[X*]{2}-\d{4}$", re.I)
# Phone numbers only when written like one. A bare 10-digit string is far more often an
# account number, and treating it as a phone put 555 in the middle of an account number.
US_PHONE = re.compile(r"^(\+?1[ .-]?)?(\(\d{3}\) ?|\d{3}[ .-])\d{3}[ .-]\d{4}$")


def plausible(original: str) -> str:
    """A same-shape, random stand-in for an identifier."""
    if SSN.match(original):
        return f"987-65-432{secrets.randbelow(10)}"
    if MASKED_SSN.match(original):
        return original[:-4] + f"432{secrets.randbelow(10)}"
    if US_PHONE.match(original):
        digits = re.sub(r"\D", "", original)
        area = digits[-10:-7]
        fake = area + "555" + f"01{secrets.randbelow(100):02d}"
        return _reshape(original, fake)
    return _random_digits(original)


def _random_digits(original: str) -> str:
    out, first = [], True
    for ch in original:
        if ch.isdigit():
            choices = [d for d in "0123456789" if d != ch and not (first and d == "0")]
            out.append(secrets.choice(choices))
            first = False
        else:
            out.append(ch)
    return "".join(out)


def _reshape(template: str, digits: str) -> str:
    """Pour digits into template's layout, right-aligned, keeping its separators."""
    it = iter(digits.rjust(sum(c.isdigit() for c in template), "1"))
    return "".join(next(it) if c.isdigit() else c for c in template)


def reformat(value: str, template: str) -> str:
    """Rewrite value's digits in another format of the same identifier.

    reformat('4815926037', '70 023 651 18') -> '48 159 260 37'
    """
    return _reshape(template, re.sub(r"\D", "", value))


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(f"{arg}\t{plausible(arg)}")
