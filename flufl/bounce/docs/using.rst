==============================
Using the flufl.bounce library
==============================

The ``flufl.bounce`` library provides a set of heuristic detectors for
discerning the original bouncing email address from a bounce message.  It
contains detectors for a wide variety of formats found in the wild over the
last 15 years, as well as standard formats such as VERP_ and RFC 3464 (DSN_).
It also provides an API for extension with your own detector formats.


Basic usage
===========

In the most basic form of use, you can just pass an email message to the
top-level function, and get back a set of email addresses detected as
bouncing.

In Python 3, you should parse the message in binary (i.e. bytes) mode using
say `email.message_from_bytes()`.  You will get back a set of byte addresses.
In Python 2, you should use `email.message_from_string()` to parse the
message, and you will get back 8-bit strings.

Here for example, is a simple DSN-like bounce message.  `parse()` is the
appropriate email parsing function described above.

    >>> msg = parse(b"""\
    ... From: Mail Delivery Subsystem <mailer-daemon@example.com>
    ... To: list-bounces@example.com
    ... Subject: Delivery Report
    ... MIME-Version: 1.0
    ... Content-Type: multipart/report; report-type=delivery-status;
    ...     boundary=AAA
    ...
    ... --AAA
    ... Content-Type: message/delivery-status
    ...
    ... Original-Recipient: rfc822;anne@example.com
    ... Action: failed
    ...
    ... Original-Recipient: rfc822;bart@example.com
    ... Action: delayed
    ...
    ... --AAA--
    ... """)

..
    >>> def print_emails(recipients):
    ...     if recipients is None:
    ...         print('None')
    ...         return
    ...     if len(recipients) == 0:
    ...         print('No addresses')
    ...     for email in sorted(recipients):
    ...         # Remove the Py3 extraneous b'' prefixes.
    ...         if bytes is not str:
    ...             email = repr(email)[2:-1]
    ...         print(email)

You can scan the bounce message object to get a set of all the email addresses
that have permanent failures.

    >>> from flufl.bounce import scan_message
    >>> recipients = scan_message(msg)
    >>> print_emails(recipients)
    anne@example.com

You can also get the set of all temporarily and permanent failures.

    >>> from flufl.bounce import all_failures
    >>> temporary, permanent = all_failures(msg)
    >>> print_emails(temporary)
    bart@example.com
    >>> print_emails(permanent)
    anne@example.com


.. _VERP: http://en.wikipedia.org/wiki/Variable_envelope_return_path
.. _DSN: http://www.faqs.org/rfcs/rfc3464.html
