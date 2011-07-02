==============================
Using the flufl.bounce library
==============================

The ``flufl.bounce`` library provides a set of heuristic detectors for
discerning the original bouncing recipient from a bounce message.  It contains
detectors for a wide variety of formats found in the wild over the last 15
years, as well as standard formats such as VERP_ and RFC 3464 (DSN_).  It also
provides an API for extension with your own detector formats.


Basic usage
===========

In the most basic form of use, you can just pass an email message to the
top-level function, and get back a set of email addresses detected as
bouncing.  Here for example, is a simple DSN-like bounce message:

    >>> from email import message_from_string as parse
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
    ...         print 'None'
    ...         return
    ...     for email in sorted(recipients):
    ...         print email

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
