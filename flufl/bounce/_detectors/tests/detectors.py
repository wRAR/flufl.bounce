# Copyright (C) 2011-2012 by Barry A. Warsaw
#
# This file is part of flufl.bounce
#
# flufl.bounce is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# flufl.bounce is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with flufl.bounce.  If not, see <http://www.gnu.org/licenses/>.

"""Test the bounce detection modules."""

from __future__ import absolute_import, unicode_literals

__metaclass__ = type
__all__ = [
    'make_test_cases',
    ]


import sys
import unittest

from contextlib import closing
try:
    # Python 3.2
    from email import message_from_binary_file as parse
except ImportError:
    # Python 2
    from email import message_from_file as parse
from pkg_resources import resource_stream


COMMASPACE = b', '



class BounceTestCase(unittest.TestCase):
    """Test a single bounce detection."""

    def __init__(self, bounce_module, sample_file,
                 expected, is_temporary=False):
        """See `unittest.TestCase`."""
        unittest.TestCase.__init__(self)
        self.bounce_module = bounce_module
        self.sample_file = sample_file
        self.expected = set(expected)
        self.is_temporary = is_temporary

    def setUp(self):
        """See `unittest.TestCase`."""
        module_name = 'flufl.bounce._detectors.' + self.bounce_module
        __import__(module_name)
        self.module = sys.modules[module_name]
        with closing(resource_stream('flufl.bounce.tests.data',
                                     self.sample_file)) as fp:
            self.message = parse(fp)

    def shortDescription(self):
        """See `unittest.TestCase`."""
        expected = COMMASPACE.join(sorted(self.expected))
        return '{0}: [{1}] detecting {2} in {3}'.format(
            self.bounce_module,
            ('T' if self.is_temporary else 'P'),
            expected, self.sample_file)

    def __str__(self):
        # XXX Ugly disgusting hack to make both unittest and zope.testrunner
        # 'work'.  The former uses str() to determine whether the test should
        # run while the latter uses str() as the thing to print under verbose
        # output.  The two are not entirely compatible.
        return self.shortDescription()

    def runTest(self):
        """Test one bounce detection."""
        missing = object()
        for name in getattr(self.module, '__all__', []):
            component_class = getattr(self.module, name, missing)
            if component_class is missing:
                raise RuntimeError(
                    'skipping missing __all__ entry: {0}'.format(name))
            component = component_class()
            # XXX 2011-07-02: We don't currently test temporary failures.
            temporary, permanent = component.process(self.message)
            got = (set(temporary) if self.is_temporary else set(permanent))
            self.assertEqual(got, self.expected)



def make_test_cases():
    for data in DATA:
        if len(data) == 3:
            module, filename, expected = data
            is_temporary = False
        else:
            module, filename, expected, is_temporary = data
        test = BounceTestCase(module, filename, expected, is_temporary)
        yield test



DATA = (
    # Postfix bounces
    ('postfix', 'postfix_01.txt', [b'xxxxx@local.ie']),
    ('postfix', 'postfix_02.txt', [b'yyyyy@digicool.com']),
    ('postfix', 'postfix_03.txt', [b'ttttt@ggggg.com']),
    ('postfix', 'postfix_04.txt', [b'davidlowie@mail1.keftamail.com']),
    ('postfix', 'postfix_05.txt', [b'bjelf@detectit.net']),
    # Exim bounces
    ('exim', 'exim_01.txt', [b'delangen@its.tudelft.nl']),
    # SimpleMatch bounces
    ('simplematch', 'sendmail_01.txt', [b'zzzzz@nfg.nl']),
    ('simplematch', 'simple_01.txt', [b'bbbsss@turbosport.com']),
    ('simplematch', 'simple_02.txt', [b'chris.ggggmmmm@usa.net']),
    ('simplematch', 'simple_04.txt', [b'claird@starbase.neosoft.com']),
    ('simplematch', 'newmailru_01.txt', [b'zzzzz@newmail.ru']),
    ('simplematch', 'hotpop_01.txt', [b'allensmithee@hotpop.com']),
    ('simplematch', 'microsoft_03.txt', [b'midica@banknbr.com']),
    ('simplematch', 'simple_05.txt', [b'rlosardo@sbcglobal.net']),
    ('simplematch', 'simple_06.txt', [b'dlyle@hamiltonpacific.com']),
    ('simplematch', 'simple_07.txt', [b'william.xxxx@sbcglobal.net']),
    ('simplematch', 'simple_08.txt', [b'severin.XXX@t-online.de']),
    ('simplematch', 'simple_09.txt', [b'RobotMail@auto-walther.de']),
    ('simplematch', 'simple_10.txt', [b'sais@thehartford.com']),
    ('simplematch', 'simple_11.txt', [b'carlosr73@hartfordlife.com']),
    ('simplematch', 'simple_12.txt', [b'charrogar@rhine1.andrew.ac.jp']),
    ('simplematch', 'simple_13.txt', [b'dycusibreix@ademe.fr']),
    ('simplematch', 'simple_14.txt', [b'dump@dachamp.com',
                                      b'iqxwmmfauudpo@dachamp.com']),
    ('simplematch', 'simple_15.txt', [b'isam@kviv.be']),
    ('simplematch', 'simple_16.txt', [b'xvlogtfsei@the-messenger.com']),
    ('simplematch', 'simple_17.txt', [b'internetsailing@gmail.com']),
    ('simplematch', 'simple_18.txt', [b'powell@kesslersupply.com']),
    ('simplematch', 'simple_19.txt', [b'mcfall@cepi.com.ar']),
    ('simplematch', 'simple_20.txt', [b'duke@ald.socgen.com']),
    ('simplematch', 'simple_23.txt', [b'ketchuy@dadoservice.it']),
    ('simplematch', 'simple_24.txt', [b'liberty@gomaps.com']),
    ('simplematch', 'simple_25.txt', [b'mahau@cnbearing.com']),
    ('simplematch', 'simple_26.txt', [b'reilizavet@lar.ieo.it']),
    ('simplematch', 'simple_27.txt', [b'kulp@webmail.pla.net.py']),
    ('simplematch', 'simple_29.txt', [b'thilakayi_bing@landshire.com']),
    ('simplematch', 'simple_30.txt', [b'wmnqicorpat@nqicorp.com']),
    ('simplematch', 'simple_31.txt', [b'nmorel@actisce.fr']),
    ('simplematch', 'simple_32.txt', [b'teteyn@agence-forbin.com']),
    ('simplematch', 'simple_33.txt', [b'hmu@extralumin.com']),
    ('simplematch', 'simple_34.txt', [b'roland@xxx.com']),
    ('simplematch', 'simple_36.txt', [b'garyt@xxx.com']),
    ('simplematch', 'simple_37.txt', [b'user@uci.edu']),
    ('simplematch', 'bounce_02.txt', [b'acinsp1@midsouth.rr.com']),
    ('simplematch', 'bounce_03.txt', [b'james@jeborall.demon.co.uk']),
    # SimpleWarning
    ('simplewarning', 'simple_03.txt', [b'jacobus@geo.co.za'], True),
    ('simplewarning', 'simple_21.txt', [b'assumpeatman@dsgmfg.com'], True),
    ('simplewarning', 'simple_22.txt', [b'RLipton@prev.org'], True),
    ('simplewarning', 'simple_28.txt', [b'luis.hiam@gmail.com'], True),
    ('simplewarning', 'simple_35.txt', [b'calvin@xxx.com'], True),
    # GroupWise
    ('groupwise', 'groupwise_01.txt', [b'thoff@MAINEX1.ASU.EDU']),
    # This one really sucks 'cause it's text/html.  Just make sure it
    # doesn't throw an exception, but we won't get any meaningful
    # addresses back from it.
    ('groupwise', 'groupwise_02.txt', []),
    # Actually, it's from Exchange, and Exchange does recognize it
    ('exchange', 'groupwise_02.txt', [b'omarmo@thebas.com']),
    # Yale's own
    ('yale', 'yale_01.txt', [b'thomas.dtankengine@cs.yale.edu',
                             b'thomas.dtankengine@yale.edu']),
    # DSN, i.e. RFC 1894
    ('dsn', 'dsn_01.txt', [b'JimmyMcEgypt@go.com']),
    ('dsn', 'dsn_02.txt', [b'zzzzz@zeus.hud.ac.uk']),
    ('dsn', 'dsn_03.txt', [b'ddd.kkk@advalvas.be']),
    ('dsn', 'dsn_04.txt', [b'max.haas@unibas.ch']),
    ('dsn', 'dsn_05.txt', [b'pkocmid@atlas.cz'], True),
    ('dsn', 'dsn_06.txt', [b'hao-nghi.au@fr.thalesgroup.com'], True),
    ('dsn', 'dsn_07.txt', [b'david.farrar@parliament.govt.nz'], True),
    ('dsn', 'dsn_08.txt',
      [b'news-list.zope@localhost.bln.innominate.de'], True),
    ('dsn', 'dsn_09.txt', [b'pr@allen-heath.com']),
    ('dsn', 'dsn_10.txt', [b'anne.person@dom.ain']),
    ('dsn', 'dsn_11.txt', [b'joem@example.com']),
    ('dsn', 'dsn_12.txt', [b'auaauqdgrdz@jtc-con.co.jp']),
    ('dsn', 'dsn_13.txt', [b'marcooherbst@cardinal.com']),
    ('dsn', 'dsn_14.txt', [b'artboardregistration@home.dk']),
    ('dsn', 'dsn_15.txt', [b'horu@ccc-ces.com']),
    ('dsn', 'dsn_16.txt', [b'hishealinghand@pastors.com']),
    ('dsn', 'dsn_17.txt', [b'christine.barsas@sivarikeskus.fi'], True),
    # Microsoft Exchange
    ('exchange', 'microsoft_01.txt', [b'DJBENNETT@IKON.COM']),
    ('exchange', 'microsoft_02.txt', [b'MDMOORE@BALL.COM']),
    # SMTP32
    ('smtp32', 'smtp32_01.txt', [b'oliver@pcworld.com.ph']),
    ('smtp32', 'smtp32_02.txt', [b'lists@mail.spicynoodles.com']),
    ('smtp32', 'smtp32_03.txt', [b'borisk@gw.xraymedia.com']),
    ('smtp32', 'smtp32_04.txt', [b'after_another@pacbell.net',
                                 b'one_bad_address@pacbell.net']),
    ('smtp32', 'smtp32_05.txt', [b'jmrpowersports@jmrpowersports.com']),
    ('smtp32', 'smtp32_06.txt', [b'Absolute_garbage_addr@pacbell.net']),
    ('smtp32', 'smtp32_07.txt', [b'info@husbyran.com']),
    # Qmail
    ('qmail', 'qmail_01.txt', [b'psadisc@wwwmail.n-h.de']),
    ('qmail', 'qmail_02.txt', [b'rauschlo@frontfin.com']),
    ('qmail', 'qmail_03.txt', [b'crown@hbc.co.jp']),
    ('qmail', 'qmail_04.txt', [b'merotiia@tennisnsw.com.au']),
    ('qmail', 'qmail_05.txt', [b'ivokggrrdvc@caixaforte.freeservers.com']),
    ('qmail', 'qmail_06.txt', [b'ntl@xxx.com']),
    ('qmail', 'qmail_07.txt', [b'user@example.net']),
    # LLNL's custom Sendmail
    ('llnl', 'llnl_01.txt', [b'trotts1@llnl.gov']),
    # Netscape's server...
    ('netscape', 'netscape_01.txt', [b'aaaaa@corel.com',
                                     b'bbbbb@corel.com']),
    # Yahoo's proprietary format
    ('yahoo', 'yahoo_01.txt', [b'subscribe.motorcycles@listsociety.com']),
    ('yahoo', 'yahoo_02.txt', [b'agarciamartiartu@yahoo.es']),
    ('yahoo', 'yahoo_03.txt', [b'cresus22@yahoo.com']),
    ('yahoo', 'yahoo_04.txt', [b'agarciamartiartu@yahoo.es',
                               b'open00now@yahoo.co.uk']),
    ('yahoo', 'yahoo_05.txt', [b'cresus22@yahoo.com',
                               b'jjb700@yahoo.com']),
    ('yahoo', 'yahoo_06.txt', [b'andrew_polevoy@yahoo.com',
                               b'baruch_sterin@yahoo.com',
                               b'rjhoeks@yahoo.com',
                               b'tritonrugger91@yahoo.com']),
    ('yahoo', 'yahoo_07.txt', [b'mark1960_1998@yahoo.com',
                               b'ovchenkov@yahoo.com',
                               b'tsa412@yahoo.com',
                               b'vaxheadroom@yahoo.com']),
    ('yahoo', 'yahoo_08.txt', [b'chatrathis@yahoo.com',
                               b'crownjules01@yahoo.com',
                               b'cwl_999@yahoo.com',
                               b'eichaiwiu@yahoo.com',
                               b'rjhoeks@yahoo.com',
                               b'yuli_kolesnikov@yahoo.com']),
    ('yahoo', 'yahoo_09.txt', [b'hankel_o_fung@yahoo.com',
                               b'ultravirus2001@yahoo.com']),
    ('yahoo', 'yahoo_10.txt', [b'jajcchoo@yahoo.com',
                               b'lyons94706@yahoo.com',
                               b'turtle4jne@yahoo.com']),
    # sina.com appears to use their own weird SINAEMAIL MTA
    ('sina', 'sina_01.txt', [b'boboman76@sina.com', 
                             b'alan_t18@sina.com']),
    ('aol', 'aol_01.txt', [b'screenname@aol.com']),
    # No address can be detected in these...
    # dumbass_01.txt - We love Microsoft. :(
    # Done
    )
