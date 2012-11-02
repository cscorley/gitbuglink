Some notes.
===========

Current regex usage:

`git log --oneline | grep -P "(?:bug|fix|pr)\\s*(?:id|[#=])?\\s*([0-9]{4,6})"`

Mylyn
-----

Seems to have each commit tagged with a bug number, some are marked new/resolved/reopened. 

Tomcat
------

Has URL's that do not match the regex

39c4270 Fix https://issues.apache.org/bugzilla/show_bug.cgi?id=53993 Avoid NPE when the session is invalidated

Ant
---

c791b67 BR 53550, thanks to Tim Pokorny ...
33ad810 #53622: faster VectorSet.retainAll.
7fec30d Stronger tests in preparation for #53622.
328a7da Bug 51792 - Unable to override system properties with 1.8.2
d106278 problems 49079, 48961
4102c3d bugzilla 48932, IO error sending mail with plain mimetype, socket closed
269a4d add a test for issue 32461
4a6f513 bz 44493 <sql> task cannot differentiate between "no resources specified" and "no resources found"
3b39f97 43799


Rhino
-----

49648dc Merge pull request #83 from anba/bug-784358
76adbd7 Different fix for https://github.com/mozilla/rhino/pull/48
d75957d Fixes Issue 178 : Incorrect line number reporting
9ff4e34 Merge pull request #28 from autre/master
Some commit messages have the entire bug report pasted in. Norris Boyd, damn you!

Eclipse
-------

8bf2a98 http://dev.eclipse.org/bugs/show_bug.cgi?id=12960
5f4e8fd 20063
7ccbf75 change to 20154 fix
f803102 DLL 25719
71a1f7f defect 38275

Several commits have two bug numbers
e7844f9 Code formatted Bug 23482 - Rework the Core Ant code to be able to use the NLS tools Bug 14180 - Ant -help not function
d739074 Code formatted Bug 23482 - Rework the Core Ant code to be able to use the NLS tools Bug 23350 - Possible NPE
26ffc71 Code formatted Bug 23482 - Rework the Core Ant code to be able to use the NLS tools Bug 23382 - API - Add @since tags

### jdt

50c2200 Backed out changes made for [35699]
6dfd27d [35699]

### pde

f6f8717 defects 39508, 39509, 39510
