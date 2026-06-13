# no debug infos with:
%global debug_package %{nil}

# disable check-buildroot (normally /usr/lib/rpm/check-buildroot) with:
%define __arch_install_post %{nil}

%define __os_install_post %{nil}

# disable automatic dependency and provides generation with:
%define __find_provides %{nil} 
%define __find_requires %{nil} 
%define _use_internal_dependency_generator 0
Autoprov: 0
Autoreq: 0

Name: sudomock
Summary: sudomock
Version: 1.0
Release: 2%{?dist}
Group: System Environment/Base
License: GPL-2.0-or-later AND LGPL-2.1-or-later
URL: https://copr.fedorainfracloud.org/coprs/amidevous/rpmsoftwarecollection/builds/

Requires(post): systemd
Requires(post): systemd-udev
Requires(post): /usr/sbin/update-alternatives
Requires(preun): systemd
Requires(preun): /usr/sbin/update-alternatives
Requires(postun): systemd
Requires: scl-utils-build wget dnf sudo


%description
sudomock
sudomock.







%install
mkdir -p $RPM_BUILD_ROOT
touch $RPM_BUILD_ROOT/sudomock

%post
cat /etc/sudoers > /etc/sudoers.bk
echo "mock ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
echo "mockbuild ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
echo "mock-build ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
sleep 10
sudo echo "root"
sleep 10
echo "no root"
sleep 10




%files
/sudomock



%changelog
* Thu May 7 2026 Rahul Rajesh <rrajesh@redhat.com> - 1.0-1
- add package
