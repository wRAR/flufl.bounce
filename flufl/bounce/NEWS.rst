=====================
NEWS for flufl.bounce
=====================

1.0.2 (2011-10-10)
==================
 * Fixed MANIFEST.in to exclude the .egg.


1.0.1 (2011-10-07)
==================
 * Fixed licenses.  All code is LGPLv3.


1.0 (2011-08-22)
================
 * Initial release.


0.91 (2011-07-15)
=================
 * Provide a nicer interface for detector modules.  Instead of using the magic
   empty tuple returns, provide three convenience constants in the interfaces
   module: NoFailures, NoTemporaryFailures, and NoPermanentFailures.
 * Add logging support.  Applications can initialize the `flufl.bounce`
   logger.  The test suite does its own logging.basicConfig(), which can be
   influenced by the environment variable $FLUFL_LOGGING.  See
   flufl/bounce/tests/helpers.py for details.


0.90 (2011-07-02)
=================
 * Initial refactoring from Mailman 3.
