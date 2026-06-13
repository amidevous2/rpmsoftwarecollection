%{?scl:%scl_package openssl}
%{!?scl:%global pkg_name %{name}}
%{?scl:%global _scl_vendor remi}
%{?scl:%global _vendor remi}

# no debug infos with:
#%#global debug_package %{nil}

# disable check-buildroot (normally /usr/lib/rpm/check-buildroot) with:
%define __arch_install_post %{nil}

%define __os_install_post %{nil}

# disable automatic dependency and provides generation with:
%define __find_provides %{nil} 
%define __find_requires %{nil} 
%define _use_internal_dependency_generator 0
Autoprov: 0
Autoreq: 0

# For the curious:
# 0.9.5a soversion = 0
# 0.9.6  soversion = 1
# 0.9.6a soversion = 2
# 0.9.6c soversion = 3
# 0.9.7a soversion = 4
# 0.9.7ef soversion = 5
# 0.9.8ab soversion = 6
# 0.9.8g soversion = 7
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
# 1.1.0 soversion = 1.1 (same as upstream although presence of some symbols
#                        depends on build configuration options)
%define soversion 1.1

# Arches on which we need to prevent arch conflicts on opensslconf.h, must
# also be handled in opensslconf-new.h.
%define multilib_arches %{ix86} ia64 %{mips} ppc ppc64 s390 s390x sparcv9 sparc64 x86_64

%global _performance_build 1

Summary: Utilities from the general purpose cryptography library with TLS implementation
Name: php56-openssl
Version: 1.1.1k
Release: 5%{?dist}
Epoch: 1
# We have to remove certain patented algorithms from the openssl source
# tarball with the hobble-openssl script which is included below.
# The original openssl upstream tarball cannot be shipped in the .src.rpm.
Source: https://github.com/amidevous2/rpmsoftwarecollection/releases/download/download/openssl-%{version}-hobbled.tar.xz
Source1: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/hobble-openssl
Source2: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/Makefile.certificate
Source6: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/make-dummy-cert
Source7: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/renew-dummy-cert
Source12: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/ec_curve.c
Source13: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/ectest.c
# Build changes
Patch1: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-build.patch
Patch2: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-defaults.patch
Patch3: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-no-html.patch
Patch4: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-man-rename.patch

# Functionality changes
Patch31: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-conf-paths.patch
Patch32: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-version-add-engines.patch
Patch33: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-apps-dgst.patch
Patch36: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-no-brainpool.patch
Patch37: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-ec-curves.patch
Patch38: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-no-weak-verify.patch
Patch40: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-disable-ssl3.patch
Patch41: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-system-cipherlist.patch
Patch42: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-fips.patch
Patch45: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-weak-ciphers.patch
Patch46: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-seclevel.patch
Patch47: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-ts-sha256-default.patch
Patch48: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-fips-post-rand.patch
Patch49: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-evp-kdf.patch
Patch50: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-ssh-kdf.patch
Patch51: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-intel-cet.patch
Patch60: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-krb5-kdf.patch
Patch61: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-edk2-build.patch
Patch62: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-fips-curves.patch
Patch65: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-fips-drbg-selftest.patch
Patch66: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-fips-dh.patch
Patch67: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-kdf-selftest.patch
Patch69: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-alpn-cb.patch
Patch70: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-rewire-fips-drbg.patch
Patch71: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-new-config-file.patch
# This modifies code that was patched before, but removing all FIPS patches
# comes with a much greater risk of introducing regressions.
Patch72: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-disable-fips.patch

# Backported fixes including security fixes
Patch52: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-s390x-update.patch
Patch53: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-fips-crng-test.patch
Patch55: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-arm-update.patch
Patch56: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-s390x-ecc.patch
Patch73: https://raw.githubusercontent.com/amidevous2/rpmsoftwarecollection/refs/heads/main/compat-openssl11/openssl-1.1.1-cve-2022-0778.patch

License: OpenSSL and ASL 2.0
URL: http://www.openssl.org/



%if 0%{?fedora} < 35 && 0%{?rhel} < 9
%{?scl:Requires: %{scl}-runtime}
%{?scl:BuildRequires: %{scl}-runtime}
BuildRequires: make
BuildRequires: gcc
BuildRequires: coreutils, perl-interpreter, sed, zlib-devel, /usr/bin/cmp
BuildRequires: lksctp-tools-devel
BuildRequires: /usr/bin/rename
BuildRequires: /usr/bin/pod2man
BuildRequires: /usr/sbin/sysctl
BuildRequires: perl(Test::Harness), perl(Test::More), perl(Math::BigInt)
BuildRequires: perl(Module::Load::Conditional), perl(File::Temp)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(FindBin), perl(lib), perl(File::Compare), perl(File::Copy)
Requires: coreutils, crypto-policies
Requires: %{?scl_prefix}openssl, %{?scl_prefix}openssl-libs
%else
BuildRequires: make
BuildRequires: gcc
BuildRequires: coreutils, perl-interpreter, sed, zlib-devel, /usr/bin/cmp
BuildRequires: lksctp-tools-devel
BuildRequires: /usr/bin/rename
BuildRequires: /usr/bin/pod2man
BuildRequires: /usr/sbin/sysctl
BuildRequires: perl(Test::Harness), perl(Test::More), perl(Math::BigInt)
BuildRequires: perl(Module::Load::Conditional), perl(File::Temp)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(FindBin), perl(lib), perl(File::Compare), perl(File::Copy)
Requires: coreutils, crypto-policies
%{?scl:Conflicts: openssl < 1:3.0, openssl-libs < 1:3.0}
%endif





%description
The OpenSSL toolkit provides support for secure communications between
machines. This version of OpenSSL package contains only the libraries
from the 1.1.1 version and is provided for compatibility with previous
releases.


%package devel
Summary: Development package for %{pkg_name}
Requires: %{?scl_prefix}%{name} = %{epoch}:%{version}-%{release}
%if 0%{?fedora} < 35 && 0%{?rhel} < 9
Requires: %{?scl_prefix}openssl-devel
%endif



%description devel
Development package for %{pkg_name}.


%prep
%{?scl:scl enable %{scl} - << \EOF}
set -ex
%setup -q -n openssl-%{version}
#%#if 0%{?fedora} < 35 && 0%{?rhel} < 9
#echo "no build"
#%#else
# The hobble_openssl is called here redundantly, just to be sure.
# The tarball has already the sources removed.
chmod +x %{SOURCE1}
%{SOURCE1} > /dev/null
cp %{SOURCE12} crypto/ec/
cp %{SOURCE13} test/
%patch -P 1 -p1 -b .build   %{?_rawbuild}
%patch -P 2 -p1 -b .defaults
%patch -P 3 -p1 -b .no-html  %{?_rawbuild}
%patch -P 4 -p1 -b .man-rename
%patch -P 31 -p1 -b .conf-paths
%patch -P 32 -p1 -b .version-add-engines
%patch -P 33 -p1 -b .dgst
%patch -P 36 -p1 -b .no-brainpool
%patch -P 37 -p1 -b .curves
%patch -P 38 -p1 -b .no-weak-verify
%patch -P 40 -p1 -b .disable-ssl3
%patch -P 41 -p1 -b .system-cipherlist
%patch -P 42 -p1 -b .fips
%patch -P 45 -p1 -b .weak-ciphers
%patch -P 46 -p1 -b .seclevel
%patch -P 47 -p1 -b .ts-sha256-default
%patch -P 48 -p1 -b .fips-post-rand
%patch -P 49 -p1 -b .evp-kdf
%patch -P 50 -p1 -b .ssh-kdf
%patch -P 51 -p1 -b .intel-cet
%patch -P 52 -p1 -b .s390x-update
%patch -P 53 -p1 -b .crng-test
%patch -P 55 -p1 -b .arm-update
%patch -P 56 -p1 -b .s390x-ecc
%patch -P 60 -p1 -b .krb5-kdf
%patch -P 61 -p1 -b .edk2-build
%patch -P 62 -p1 -b .fips-curves
%patch -P 65 -p1 -b .drbg-selftest
%patch -P 66 -p1 -b .fips-dh
%patch -P 67 -p1 -b .kdf-selftest
%patch -P 69 -p1 -b .alpn-cb
%patch -P 70 -p1 -b .rewire-fips-drbg
%patch -P 71 -p1 -b .conf-new
%patch -P 72 -p1 -b .disable-fips
%patch -P 73 -p1 -b .cve-2022-0778
cp apps/openssl.cnf apps/openssl11.cnf
#%#endif
%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - << \EOF}
set -ex
#%#if 0%{?fedora} < 35 && 0%{?rhel} < 9
#echo "no build"
#%#else
# Figure out which flags we want to use.
# default
sslarch=%{_os}-%{_target_cpu}
%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i686 ; then
	sslflags="no-asm 386"
fi
%endif
%ifarch x86_64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sparcv9
sslarch=linux-sparcv9
sslflags=no-asm
%endif
%ifarch sparc64
sslarch=linux64-sparcv9
sslflags=no-asm
%endif
%ifarch alpha alphaev56 alphaev6 alphaev67
sslarch=linux-alpha-gcc
%endif
%ifarch s390 sh3eb sh4eb
sslarch="linux-generic32 -DB_ENDIAN"
%endif
%ifarch s390x
sslarch="linux64-s390x"
%endif
%ifarch %{arm}
sslarch=linux-armv4
%endif
%ifarch aarch64
sslarch=linux-aarch64
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch sh3 sh4
sslarch=linux-generic32
%endif
%ifarch ppc64 ppc64p7
sslarch=linux-ppc64
%endif
%ifarch ppc64le
sslarch="linux-ppc64le"
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch mips mipsel
sslarch="linux-mips32 -mips32r2"
%endif
%ifarch mips64 mips64el
sslarch="linux64-mips64 -mips64r2"
%endif
%ifarch mips64el
sslflags=enable-ec_nistp_64_gcc_128
%endif
%ifarch riscv64
sslarch=linux-generic64
%endif

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
# Also add -DPURIFY to make using valgrind with openssl easier as we do not
# want to depend on the uninitialized memory as a source of entropy anyway.
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wa,--noexecstack -Wa,--generate-missing-build-notes=yes -DPURIFY $RPM_LD_FLAGS"

export HASHBANGPERL=/usr/bin/perl

# ia64, x86_64, ppc are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
./Configure \
	--prefix=%{_prefix} --openssldir=%{_sysconfdir}/pki/tls ${sslflags} \
	--system-ciphers-file=%{_sysconfdir}/crypto-policies/back-ends/openssl.config \
	zlib enable-camellia enable-seed enable-rfc3779 enable-sctp \
	enable-cms enable-md2 enable-rc5 enable-ssl3 enable-ssl3-method \
	enable-weak-ssl-ciphers \
	no-mdc2 no-ec2m no-sm2 no-sm4 \
	shared  ${sslarch} $RPM_OPT_FLAGS '-DDEVRANDOM="\"/dev/urandom\""'

# Do not run this in a production package the FIPS symbols must be patched-in
#util/mkdef.pl crypto update

make all

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done
#%#endif


%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - << \EOF}
set -ex

#%#if 0%{?fedora} < 35 && 0%{?rhel} < 9
#mkdir -p $RPM_BUILD_ROOT/usr/bin/
#touch $RPM_BUILD_ROOT/usr/bin/compat-openssl11
#touch $RPM_BUILD_ROOT/usr/bin/compat-openssl11-devel
#%#else
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
install -d $RPM_BUILD_ROOT{%{_bindir},%{_includedir},%{_libdir},%{_mandir},%{_libdir}/openssl,%{_pkgdocdir}}
%make_install
#rename so.%{soversion} so.%{version} $RPM_BUILD_ROOT%{_libdir}/*.so.%{soversion}
#for lib in $RPM_BUILD_ROOT%{_libdir}/*.so.%{version} ; do
#	chmod 755 ${lib}
#	ln -s -f `basename ${lib}` $RPM_BUILD_ROOT%{_libdir}/`basename ${lib} .%{version}`.%{soversion}
#done
# Install compat config file
install -m 644 apps/openssl11.cnf $RPM_BUILD_ROOT%{_sysconfdir}/pki/tls/openssl11.cnf
#%#endif
%{?scl:EOF}


%files
#%#if 0%{?fedora} < 35 && 0%{?rhel} < 9
#/usr/bin/compat-openssl11
#%#else
%license LICENSE
%doc FAQ NEWS README
#%attr(0755,root,root) %{_libdir}/libcrypto.so.%{version}
#%attr(0755,root,root) %{_libdir}/libcrypto.so.%{soversion}
#%attr(0755,root,root) %{_libdir}/libssl.so.%{version}
#%attr(0755,root,root) %{_libdir}/libssl.so.%{soversion}
#%attr(0755,root,root) %{_libdir}/engines-%{soversion}
%config(noreplace) %{_sysconfdir}/pki/tls/openssl11.cnf
%dir %{_sysconfdir}/pki/tls
%attr(0644,root,root) %{_sysconfdir}/pki/tls/openssl11.cnf
#%#endif



%files devel
#%#if 0%{?fedora} < 35 && 0%{?rhel} < 9
#/usr/bin/compat-openssl11-devel
#%#else
%{_libdir}/openssl
%{_includedir}/openssl
#%#endif


%ldconfig_scriptlets


%changelog
* Mon May 30 2022 Clemens Lang <cllang@redhat.com> - 1:1.1.1k-4
- Fixes CVE-2022-0778 openssl: Infinite loop in BN_mod_sqrt() reachable when parsing certificates
  Resolves: rhbz#2063147
- Disable FIPS mode; it does not work and will not be certified
  Resolves: rhbz#2091968

* Tue Oct 05 2021 Sahana Prasad <sahana@redhat.com> - 1:1.1.1k-3
- updates OPENSSL_CONF to openssl11.cnf.
- Related: rhbz#1947584, rhbz#2003123

* Mon Aug 16 2021 Sahana Prasad <sahana@redhat.com> - 1:1.1.1k-2
- Remove support for building FIPS mode binaries for the
  compat libraries
- Ships openssl11.cnf as the configuration file.
- Resolves: rhbz#1993795
- Related: rhbz#1947584

* Thu Apr 08 2021 Sahana Prasad <sahana@redhat.com> - 1:1.1.1k-1
- Repackage old openssl 1.1.1k package into compat-openssl11
  Resolves: bz#1947584
