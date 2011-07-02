# Copyright (C) 2011 by Barry A. Warsaw
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
from email import message_from_file
from pkg_resources import resource_stream


COMMASPACE = ', '



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
            self.message = message_from_file(fp)

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
    ('postfix', 'postfix_01.txt', ['xxxxx@local.ie']),
    ('postfix', 'postfix_02.txt', ['yyyyy@digicool.com']),
    ('postfix', 'postfix_03.txt', ['ttttt@ggggg.com']),
    ('postfix', 'postfix_04.txt', ['davidlowie@mail1.keftamail.com']),
    ('postfix', 'postfix_05.txt', ['bjelf@detectit.net']),
    # Exim bounces
    ('exim', 'exim_01.txt', ['delangen@its.tudelft.nl']),
    # SimpleMatch bounces
    ('simplematch', 'sendmail_01.txt', ['zzzzz@nfg.nl']),
    ('simplematch', 'simple_01.txt', ['bbbsss@turbosport.com']),
    ('simplematch', 'simple_02.txt', ['chris.ggggmmmm@usa.net']),
    ('simplematch', 'simple_04.txt', ['claird@starbase.neosoft.com']),
    ('simplematch', 'newmailru_01.txt', ['zzzzz@newmail.ru']),
    ('simplematch', 'hotpop_01.txt', ['allensmithee@hotpop.com']),
    ('simplematch', 'microsoft_03.txt', ['midica@banknbr.com']),
    ('simplematch', 'simple_05.txt', ['rlosardo@sbcglobal.net']),
    ('simplematch', 'simple_06.txt', ['dlyle@hamiltonpacific.com']),
    ('simplematch', 'simple_07.txt', ['william.xxxx@sbcglobal.net']),
    ('simplematch', 'simple_08.txt', ['severin.XXX@t-online.de']),
    ('simplematch', 'simple_09.txt', ['RobotMail@auto-walther.de']),
    ('simplematch', 'simple_10.txt', ['sais@thehartford.com']),
    ('simplematch', 'simple_11.txt', ['carlosr73@hartfordlife.com']),
    ('simplematch', 'simple_12.txt', ['charrogar@rhine1.andrew.ac.jp']),
    ('simplematch', 'simple_13.txt', ['dycusibreix@ademe.fr']),
    ('simplematch', 'simple_14.txt', ['dump@dachamp.com',
                                      'iqxwmmfauudpo@dachamp.com']),
    ('simplematch', 'simple_15.txt', ['isam@kviv.be']),
    ('simplematch', 'simple_16.txt', ['xvlogtfsei@the-messenger.com']),
    ('simplematch', 'simple_17.txt', ['internetsailing@gmail.com']),
    ('simplematch', 'simple_18.txt', ['powell@kesslersupply.com']),
    ('simplematch', 'simple_19.txt', ['mcfall@cepi.com.ar']),
    ('simplematch', 'simple_20.txt', ['duke@ald.socgen.com']),
    ('simplematch', 'simple_23.txt', ['ketchuy@dadoservice.it']),
    ('simplematch', 'simple_24.txt', ['liberty@gomaps.com']),
    ('simplematch', 'simple_25.txt', ['mahau@cnbearing.com']),
    ('simplematch', 'simple_26.txt', ['reilizavet@lar.ieo.it']),
    ('simplematch', 'simple_27.txt', ['kulp@webmail.pla.net.py']),
    ('simplematch', 'simple_29.txt', ['thilakayi_bing@landshire.com']),
    ('simplematch', 'simple_30.txt', ['wmnqicorpat@nqicorp.com']),
    ('simplematch', 'simple_31.txt', ['nmorel@actisce.fr']),
    ('simplematch', 'simple_32.txt', ['teteyn@agence-forbin.com']),
    ('simplematch', 'simple_33.txt', ['hmu@extralumin.com']),
    ('simplematch', 'simple_34.txt', ['roland@xxx.com']),
    ('simplematch', 'simple_36.txt', ['garyt@xxx.com']),
    ('simplematch', 'simple_37.txt', ['user@uci.edu']),
    ('simplematch', 'bounce_02.txt', ['acinsp1@midsouth.rr.com']),
    ('simplematch', 'bounce_03.txt', ['james@jeborall.demon.co.uk']),
    # SimpleWarning
    ('simplewarning', 'simple_03.txt', ['jacobus@geo.co.za'], True),
    ('simplewarning', 'simple_21.txt', ['assumpeatman@dsgmfg.com'], True),
    ('simplewarning', 'simple_22.txt', ['RLipton@prev.org'], True),
    ('simplewarning', 'simple_28.txt', ['luis.hiam@gmail.com'], True),
    ('simplewarning', 'simple_35.txt', ['calvin@xxx.com'], True),
    # GroupWise
    ('groupwise', 'groupwise_01.txt', ['thoff@MAINEX1.ASU.EDU']),
    # This one really sucks 'cause it's text/html.  Just make sure it
    # doesn't throw an exception, but we won't get any meaningful
    # addresses back from it.
    ('groupwise', 'groupwise_02.txt', []),
    # Actually, it's from Exchange, and Exchange does recognize it
    ('exchange', 'groupwise_02.txt', ['omarmo@thebas.com']),
    # Yale's own
    ('yale', 'yale_01.txt', ['thomas.dtankengine@cs.yale.edu',
                             'thomas.dtankengine@yale.edu']),
    # DSN, i.e. RFC 1894
    ('dsn', 'dsn_01.txt', ['JimmyMcEgypt@go.com']),
    ('dsn', 'dsn_02.txt', ['zzzzz@zeus.hud.ac.uk']),
    ('dsn', 'dsn_03.txt', ['ddd.kkk@advalvas.be']),
    ('dsn', 'dsn_04.txt', ['max.haas@unibas.ch']),
    ('dsn', 'dsn_05.txt', ['pkocmid@atlas.cz'], True),
    ('dsn', 'dsn_06.txt', ['hao-nghi.au@fr.thalesgroup.com'], True),
    ('dsn', 'dsn_07.txt', ['david.farrar@parliament.govt.nz'], True),
    ('dsn', 'dsn_08.txt',
      ['news-list.zope@localhost.bln.innominate.de'], True),
    ('dsn', 'dsn_09.txt', ['pr@allen-heath.com']),
    ('dsn', 'dsn_10.txt', ['anne.person@dom.ain']),
    ('dsn', 'dsn_11.txt', ['joem@example.com']),
    ('dsn', 'dsn_12.txt', ['auaauqdgrdz@jtc-con.co.jp']),
    ('dsn', 'dsn_13.txt', ['marcooherbst@cardinal.com']),
    ('dsn', 'dsn_14.txt', ['artboardregistration@home.dk']),
    ('dsn', 'dsn_15.txt', ['horu@ccc-ces.com']),
    ('dsn', 'dsn_16.txt', ['hishealinghand@pastors.com']),
    ('dsn', 'dsn_17.txt', ['christine.barsas@sivarikeskus.fi'], True),
    # Microsoft Exchange
    ('exchange', 'microsoft_01.txt', ['DJBENNETT@IKON.COM']),
    ('exchange', 'microsoft_02.txt', ['MDMOORE@BALL.COM']),
    # SMTP32
    ('smtp32', 'smtp32_01.txt', ['oliver@pcworld.com.ph']),
    ('smtp32', 'smtp32_02.txt', ['lists@mail.spicynoodles.com']),
    ('smtp32', 'smtp32_03.txt', ['borisk@gw.xraymedia.com']),
    ('smtp32', 'smtp32_04.txt', ['after_another@pacbell.net',
                                 'one_bad_address@pacbell.net']),
    ('smtp32', 'smtp32_05.txt', ['jmrpowersports@jmrpowersports.com']),
    ('smtp32', 'smtp32_06.txt', ['Absolute_garbage_addr@pacbell.net']),
    ('smtp32', 'smtp32_07.txt', ['info@husbyran.com']),
    # Qmail
    ('qmail', 'qmail_01.txt', ['psadisc@wwwmail.n-h.de']),
    ('qmail', 'qmail_02.txt', ['rauschlo@frontfin.com']),
    ('qmail', 'qmail_03.txt', ['crown@hbc.co.jp']),
    ('qmail', 'qmail_04.txt', ['merotiia@tennisnsw.com.au']),
    ('qmail', 'qmail_05.txt', ['ivokggrrdvc@caixaforte.freeservers.com']),
    ('qmail', 'qmail_06.txt', ['ntl@xxx.com']),
    # LLNL's custom Sendmail
    ('llnl', 'llnl_01.txt', ['trotts1@llnl.gov']),
    # Netscape's server...
    ('netscape', 'netscape_01.txt', ['aaaaa@corel.com',
                                     'bbbbb@corel.com']),
    # Yahoo's proprietary format
    ('yahoo', 'yahoo_01.txt', ['subscribe.motorcycles@listsociety.com']),
    ('yahoo', 'yahoo_02.txt', ['agarciamartiartu@yahoo.es']),
    ('yahoo', 'yahoo_03.txt', ['cresus22@yahoo.com']),
    ('yahoo', 'yahoo_04.txt', ['agarciamartiartu@yahoo.es',
                               'open00now@yahoo.co.uk']),
    ('yahoo', 'yahoo_05.txt', ['cresus22@yahoo.com',
                               'jjb700@yahoo.com']),
    ('yahoo', 'yahoo_06.txt', ['andrew_polevoy@yahoo.com',
                               'baruch_sterin@yahoo.com',
                               'rjhoeks@yahoo.com',
                               'tritonrugger91@yahoo.com']),
    ('yahoo', 'yahoo_07.txt', ['mark1960_1998@yahoo.com',
                               'ovchenkov@yahoo.com',
                               'tsa412@yahoo.com',
                               'vaxheadroom@yahoo.com']),
    ('yahoo', 'yahoo_08.txt', ['chatrathis@yahoo.com',
                               'crownjules01@yahoo.com',
                               'cwl_999@yahoo.com',
                               'eichaiwiu@yahoo.com',
                               'rjhoeks@yahoo.com',
                               'yuli_kolesnikov@yahoo.com']),
    ('yahoo', 'yahoo_09.txt', ['hankel_o_fung@yahoo.com',
                               'ultravirus2001@yahoo.com']),
    ('yahoo', 'yahoo_10.txt', ['jajcchoo@yahoo.com',
                               'lyons94706@yahoo.com',
                               'turtle4jne@yahoo.com']),
    # sina.com appears to use their own weird SINAEMAIL MTA
    ('sina', 'sina_01.txt', ['boboman76@sina.com', 'alan_t18@sina.com']),
    ('aol', 'aol_01.txt', ['screenname@aol.com']),
    # No address can be detected in these...
    # dumbass_01.txt - We love Microsoft. :(
    # Done
    )
