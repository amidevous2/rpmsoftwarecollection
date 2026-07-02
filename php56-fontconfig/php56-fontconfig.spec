%{?scl:%scl_package fontconfig}
%{!?scl:%global pkg_name %{name}}
%{?scl:%global _scl_vendor remi}
%{?scl:%global _vendor remi}
%{?scl:%global _scl_prefix /opt/remi}
%{?scl:%global _scl_root /opt/remi/php56/root/}
%{?scl:%global _prefix /opt/remi/php56/root/usr}
%{?scl:%global _sysconfdir /opt/remi/php56/root/etc}
%{?scl:%global _exec_prefix /opt/remi/php56/root/usr}
%{?scl:%global _includedir /opt/remi/php56/root/usr/include}
%{?scl:%global _bindir /opt/remi/php56/root/usr/bin}
%{?scl:%global _sbindir /opt/remi/php56/root/usr/sbin}
%{?scl:%global _libdir /opt/remi/php56/root/usr/lib64}
%{?scl:%global _libexecdir /opt/remi/php56/root/usr/libexec}
%{?scl:%global _datadir /opt/remi/php56/root/usr/share}
%{?scl:%global _infodir /opt/remi/php56/root/usr/share/info}
%{?scl:%global _mandir /opt/remi/php56/root/usr/share/man}
%{?scl:%global _docdir /opt/remi/php56/root/usr/share/doc}


## ifdef'd in source code but runtime dep will be made for FT_Done_MM_Var symbol in freetype-2.9.1
# so update the build deps as well to keep deps consistency between runtime and build time.
%global freetype_version 2.9.1

Summary:	Font configuration and customization library
Name:		%{?scl_prefix}fontconfig
Version:	2.14.0
Release:	2.99%{?dist}
# src/ftglue.[ch] is in Public Domain
# src/fccache.c contains Public Domain code
# fc-case/CaseFolding.txt is in the UCD
# otherwise MIT
License:	MIT and Public Domain and UCD
Source:		https://github.com/amidevous2/rpmsoftwarecollection/releases/download/download/%{pkg_name}-%{version}.tar.xz
URL:		http://fontconfig.org
Source1:	25-no-bitmap-fedora.conf
Source2:	fc-cache

# https://bugzilla.redhat.com/show_bug.cgi?id=140335
Patch0:		%{pkg_name}-sleep-less.patch
Patch4:		%{pkg_name}-drop-lang-from-pkgkit-format.patch
Patch5:		%{pkg_name}-disable-network-required-test.patch
Patch6:		%{pkg_name}-revert-noto-default.patch
Patch7:		%{pkg_name}-fix-remapdir.patch

%{?scl:Requires: %{scl}-runtime}
%{?scl:BuildRequires: %{scl}-runtime}
BuildRequires:	%{?scl_prefix}libxml2-devel
BuildRequires:	freetype-devel >= %{freetype_version}
BuildRequires:	fontpackages-devel
BuildRequires:	python3
BuildRequires:	autoconf automake libtool gettext
BuildRequires:	gperf
BuildRequires:  %{?scl_prefix}docbook-utils %{?scl_prefix}docbook-utils-pdf
BuildRequires: make

Requires:	fonts-filesystem %{?scl_prefix}freetype
# Register DTD system-wide to make validation work by default
# (used by fonts-rpm-macros)
Requires(pre):    xml-common
Requires(postun): xml-common
PreReq:		freetype >= 2.9.1-6
Requires(post):	grep coreutils
Requires:	font(:lang=en)


%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.


%package	devel
Summary:	Font configuration and customization library
Requires:	%{?scl_prefix}%{pkg_name}%{?_isa} = %{version}-%{release}
Requires:	%{?scl_prefix}freetype-devel >= %{freetype_version}
Requires:	%{?scl_prefix}pkgconfig
Requires:	%{?scl_prefix}gettext


%description	devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.


%package	devel-doc
Summary:	Development Documentation files for fontconfig library
BuildArch:	noarch
Requires:	%{?scl_prefix}%{pkg_name}-devel = %{version}-%{release}


%description	devel-doc
The fontconfig-devel-doc package contains the documentation files
which is useful for developing applications that uses fontconfig.


%prep
%{?scl:scl enable %{scl} - << \EOF}
set -ex
%autosetup -n %{pkg_name}-%{version} -p1
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - << \EOF}
set -ex
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

for i in doc/*.fncs; do
  touch -r $i ${i//.fncs/.sgml}
done
autoreconf
CFLAGS=$RPM_OPT_FLAGS
CFLAGS="-I%{_includedir}/ $CFLAGS"
LDFLAGS="-L%{_libdir}/ $LDFLAGS"
PKG_CONFIG_PATH="%{_libdir}/pkgconfig:$PKG_CONFIG_PATH"
export LDFLAGS
export CFLAGS
export PKG_CONFIG_PATH
%configure	--with-add-fonts=/usr/share/X11/fonts/Type1,/usr/share/X11/fonts/TTF,/usr/local/share/fonts \
		--enable-libxml2 \
		--disable-static --with-cache-dir=%{_prefix}/lib/fontconfig/cache

make %{?_smp_mflags}
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - << \EOF}
set -ex
CFLAGS=$RPM_OPT_FLAGS
CFLAGS="-I%{_includedir}/ $CFLAGS"
LDFLAGS="-L%{_libdir}/ $LDFLAGS"
PKG_CONFIG_PATH="%{_libdir}/pkgconfig:$PKG_CONFIG_PATH"
export LDFLAGS
export CFLAGS
export PKG_CONFIG_PATH
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s %{_prefix}/share/fontconfig/conf.avail/25-unhint-nonlatin.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d

# move installed doc files back to build directory to package them
# in the right place
mv $RPM_BUILD_ROOT%{_docdir}/fontconfig/* .
rmdir $RPM_BUILD_ROOT%{_docdir}/fontconfig/

# adjust the timestamp to avoid conflicts for multilib
touch -r doc/fontconfig-user.sgml fontconfig-user.txt
touch -r doc/fontconfig-user.sgml fontconfig-user.html

# rename fc-cache binary
mv $RPM_BUILD_ROOT%{_bindir}/fc-cache $RPM_BUILD_ROOT%{_bindir}/fc-cache-%{__isa_bits}

# create link to man page
echo ".so man1/fc-cache.1" > $RPM_BUILD_ROOT%{_mandir}/man1/fc-cache-%{__isa_bits}.1

install -p -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/fc-cache

%find_lang %{pkg_name}
%find_lang %{pkg_name}-conf
cat %{pkg_name}-conf.lang >> %{pkg_name}.lang
%{?scl:EOF}


%post
%{?scl:scl enable %{scl} - << \EOF}
set -ex
umask 0022

mkdir -p %{_prefix}/lib/fontconfig/cache

[[ -d %{_localstatedir}/cache/fontconfig ]] && rm -rf %{_localstatedir}/cache/fontconfig/* 2> /dev/null || :

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
if [ -x %{_bindir}/fc-cache ] && %{_bindir}/fc-cache --version 2>&1 | grep -q %{version} ; then
  HOME=/root %{_bindir}/fc-cache -f
fi

%transfiletriggerin -- %{_prefix}/share/fonts /usr/share/X11/fonts/Type1 %{_prefix}/share/X11/fonts/TTF %{_prefix}/local/share/fonts
HOME=/root %{_bindir}/fc-cache -s

%transfiletriggerpostun -- %{_prefix}/share/fonts /usr/share/X11/fonts/Type1 %{_prefix}/share/X11/fonts/TTF %{_prefix}/local/share/fonts
HOME=/root %{_bindir}/fc-cache -s
%{?scl:EOF}


%posttrans
%{?scl:scl enable %{scl} - << \EOF}
set -ex
if [ -e %{_sysconfdir}/xml/catalog ]; then
  %{_bindir}/xmlcatalog --noout --add system \
                        "urn:fontconfig:fonts.dtd" \
                        "file://%{_datadir}/xml/fontconfig/fonts.dtd" \
                        %{_sysconfdir}/xml/catalog
fi
%{?scl:EOF}


%postun
%{?scl:scl enable %{scl} - << \EOF}
set -ex
if [ $1 == 0 ] && [ -e %{_sysconfdir}/xml/catalog ]; then
  %{_bindir}/xmlcatalog --noout --del "urn:fontconfig:fonts.dtd" %{_sysconfdir}/xml/catalog
fi
%{?scl:EOF}


%files -f %{pkg_name}.lang
%doc README AUTHORS
%doc fontconfig-user.txt fontconfig-user.html
%doc %{_sysconfdir}/fonts/conf.d/README
%license COPYING
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-cache*
%{_bindir}/fc-cat
%{_bindir}/fc-conflist
%{_bindir}/fc-list
%{_bindir}/fc-match
%{_bindir}/fc-pattern
%{_bindir}/fc-query
%{_bindir}/fc-scan
%{_bindir}/fc-validate
%{_prefix}/share/fontconfig/conf.avail/*.conf
%{_datadir}/xml/fontconfig
# fonts.conf is not supposed to be modified.
# If you want to do so, you should use local.conf instead.
#%config %{_prefix}/share/fontconfig/conf.avail/fonts.conf
%{_sysconfdir}/fonts/conf.d/*conf
%{_sysconfdir}/fonts/fonts.conf
%config(noreplace) %{_prefix}/share/fontconfig/conf.avail/*.conf
%dir %{_prefix}/lib/fontconfig/cache
%{_mandir}/man1/*
%{_mandir}/man5/*


%files devel
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig
%{_mandir}/man3/*
%{_datadir}/gettext/its/fontconfig.its
%{_datadir}/gettext/its/fontconfig.loc


%files devel-doc
%doc fontconfig-devel.txt fontconfig-devel


%changelog
* Fri Dec  2 2022 Akira TAGOH <tagoh@redhat.com> - 2.14.0-2
- Fix the wrong behavior on remap-dir in config.
  Resolves: rhbz#2150227

* Thu Mar 31 2022 Akira TAGOH <tagoh@redhat.com> - 2.14.0-1
- New upstream release.
- Rebase to 2.14 and revert Noto Default change happened in f36.
  Resolves: rhbz#2075393
