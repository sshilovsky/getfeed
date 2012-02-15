# Copyright 1999-2012 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

EAPI=4

# TODO git/src_uri decision

DESCRIPTION="RSS/Atom feed fetcher and piper"
HOMEPAGE=""
SRC_URI=""

LICENSE="BSD-4"
SLOT="0"
KEYWORDS="~alpha ~amd64 ~arm ~ia64 ~ppc ~ppc64 ~sparc ~x86 ~x86-fbsd ~x86-freebsd ~amd64-linux ~x86-linux ~x86-solaris"
IUSE=""

# TODO test with python-2.4 and later
DEPEND="
	>=dev-lang/python-2.4[sqlite]
	dev-python/pyyaml
	dev-python/pyxdg
	dev-python/feedparser"
RDEPEND="${DEPEND}"

