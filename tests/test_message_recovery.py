
from context import (
        gitbuglink
        )

import unittest

class MessageTestSuite(unittest.TestCase):

    def test_basic_bug(self):
        msg = """
        """

    def test_url_id(self):
        # from Tomcat commit 39c4270acadaf605a9201bb60b8a8ff118fccdf1
        msg = """Fix https://issues.apache.org/bugzilla/show_bug.cgi?id=53993
Avoid NPE when the session is invalidated

git-svn-id: https://svn.apache.org/repos/asf/tomcat/trunk@1397868 13f79535-47bb-0310-9956-ffa450edef68
"""

        bugs = list(gitbuglink.git.detect_message(msg))
        assert len(bugs) == 1
        assert '53993' in bugs

    def test_both_url_and_bug_id(self):
        # from Tomcat commit 80a7aff3e20045f428b33727a5277e62da6ba4d2
        msg = """Fix https://issues.apache.org/bugzilla/show_bug.cgi?id=52259
Regression caused by bug 46264. Prevent deadlock if no Realm is
configured.

git-svn-id: https://svn.apache.org/repos/asf/tomcat/trunk@1208046 13f79535-47bb-0310-9956-ffa450edef68
"""
        bugs = list(gitbuglink.git.detect_message(msg))
        assert len(bugs) == 2
        assert '52259' in bugs
        assert '46264' in bugs


    def test_br_id(self):
        # Ant commit c791b677b67b976916f543df3b2048a994941c5b
        msg = """BR 53550, thanks to Tim Pokorny
Improve the resolution of the extension point to bind to:
- first try the extension point which might be in the same file
- then try the one in the root file

Still some work to do: there might be intermediate file in the import stack which we would to resolve the name agai



git-svn-id: https://svn.apache.org/repos/asf/ant/core/trunk@1373326 13f79535-47bb-0310-9956-ffa450edef68
"""

        bugs = list(gitbuglink.git.detect_message(msg))
        assert len(bugs) == 1
        assert '53550' in bugs

    def test_hash_id(self):
        # Ant commit 33ad81017516e020cc87f2210e57d088c6ea7b44

        msg = """#53622: faster VectorSet.retainAll.

    git-svn-id: https://svn.apache.org/repos/asf/ant/core/trunk@1367741 13f79535-47bb-0310-9956-ffa450edef68
"""
        bugs = list(gitbuglink.git.detect_message(msg))
        assert len(bugs) == 1
        assert '53622' in bugs

        # Ant commit 7fec30d23e50361e31ca5852b0abb5fa96dc281f
        msg = """Stronger tests in preparation for #53622.

git-svn-id: https://svn.apache.org/repos/asf/ant/core/trunk@1367736 13f79535-47bb-0310-9956-ffa450edef68
"""

        bugs = list(gitbuglink.git.detect_message(msg))
        assert len(bugs) == 1
        assert '53622' in bugs

    def test_bug_upcase_id(self):
        # Ant commit 328a7da150274f0a7497dc777800e7492548c304
        msg = """Bug 51792 - Unable to override system properties with 1.8.2

git-svn-id: https://svn.apache.org/repos/asf/ant/core/trunk@1343304 13f79535-47bb-0310-9956-ffa450edef68
"""

        bugs = list(gitbuglink.git.detect_message(msg))
        assert len(bugs) == 1
        assert '51792' in bugs

    def test_problem_id(self):
        # 99 problems but a git ain't one HIT ME
        # Ant commit d106278b06b7a0d136793c42c8b76cf14e3adbcb
        msg = """problems 49079, 48961

Address indexOf inefficiency in PropertyHelper default propertyexpander implementation.



git-svn-id: https://svn.apache.org/repos/asf/ant/core/trunk@932588 13f79535-47bb-0310-9956-ffa450edef68
"""

        bugs = list(gitbuglink.git.detect_message(msg))
        assert len(bugs) == 2
        assert '49079' in bugs
        assert '48961' in bugs


    def test_bugzilla_id(self):
        # Ant commit 4102c3dae7fa5e3b4b1fb4cb4feb2513dcf1e373
        msg = """bugzilla 48932, IO error sending mail with plain mimetype, socket closed

git-svn-id: https://svn.apache.org/repos/asf/ant/core/trunk@924533 13f79535-47bb-0310-9956-ffa450edef68
"""
        bugs = list(gitbuglink.git.detect_message(msg))
        assert len(bugs) == 1
        assert '48932' in bugs

    def test_issue_id(self):
        # Antcommit 9269a4d0633eeb71d2abacbecd8307b2366a3a21
        msg = """add a test for issue 32461

git-svn-id: https://svn.apache.org/repos/asf/ant/core/trunk@720481 13f79535-47bb-0310-9956-ffa450edef68
"""

        bugs = list(gitbuglink.git.detect_message(msg))
        assert len(bugs) == 1
        assert '32461' in bugs

    def test_bz_id(self):
        # Ant commit 4a6f513f85c5b2d4646fcf699c381e0b68084620
        msg = """bz 44493 <sql> task cannot differentiate between "no resources specified" and "no resources found"

git-svn-id: https://svn.apache.org/repos/asf/ant/core/trunk@631430 13f79535-47bb-0310-9956-ffa450edef68
"""
        bugs = list(gitbuglink.git.detect_message(msg))
        assert len(bugs) == 1
        assert '44493' in bugs


