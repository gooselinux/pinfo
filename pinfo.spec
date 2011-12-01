Summary: An info file viewer
Name: pinfo
Version: 0.6.9
Release: 12%{?dist}
Group: System Environment/Base
License: GPLv2
URL: http://pinfo.alioth.debian.org
Source: http://alioth.debian.org/frs/download.php/1498/pinfo-%{version}.tar.bz2
Patch1: pinfo-0.6.9-xdg.patch
Patch2: pinfo-0.6.9-infosuff.patch
Patch3: pinfo-0.6.9-nogroup.patch
Patch4: pinfo-0.6.9-mansection.patch
Patch5: pinfo-0.6.9-infopath.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: ncurses-devel
Requires: xdg-utils
# for /sbin/install-info
Requires(post): info
Requires(preun): info

%description
Pinfo is an info file (or man page) viewer with a user interface
similar to the Lynx Web browser's interface.  Pinfo supports searching
using regular expressions, and is based on the ncurses library.

%prep
%setup -q
%patch1 -p1 -b .xdg
%patch2 -p1 -b .infosuff
%patch3 -p1 -b .nogroup
%patch4 -p1 -b .mansection
%patch5 -p1 -b .infopath

%build
%configure --without-readline
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
# These symbolic links conflict with actual binaries in perl-pmtools (bz 437612)
# ln -sf pinfo $RPM_BUILD_ROOT%{_bindir}/pman
# ln -sf pinfo.1 $RPM_BUILD_ROOT%{_mandir}/man1/pman.1

# This file should not be packaged
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog* NEWS README TECHSTUFF
%config(noreplace) %{_sysconfdir}/pinforc
%{_bindir}/pinfo
# %{_bindir}/pman
%{_infodir}/pinfo.info*
%{_mandir}/man1/pinfo.1*
# %{_mandir}/man1/pman.1*

%post
/sbin/install-info %{_infodir}/pinfo.info.gz %{_infodir}/dir &> /dev/null
:
 
%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/pinfo.info.gz %{_infodir}/dir &> /dev/null
fi
:

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Jan 07 2010 Miroslav Lichvar <mlichvar@redhat.com> 0.6.9-12
- fix source URL

* Thu Sep 24 2009 Miroslav Lichvar <mlichvar@redhat.com> 0.6.9-11
- suppress install-info errors (#515995)
- mark config as noreplace

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 04 2008 Miroslav Lichvar <mlichvar@redhat.com> 0.6.9-8
- modify default search path for info pages so that current
  directory is searched last (#458633)

* Tue Apr  1 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.6.9-7
- drop symbolic links to avoid file conflict with perl-pmtools (bz 437612)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.9-6
- Autorebuild for GCC 4.3

* Wed Oct 03 2007 Miroslav Lichvar <mlichvar@redhat.com> 0.6.9-5
- use xdg-utils instead of htmlview (#312471)

* Wed Aug 22 2007 Miroslav Lichvar <mlichvar@redhat.com> 0.6.9-4
- update license tag

* Fri Feb 23 2007 Miroslav Lichvar <mlichvar@redhat.com> 0.6.9-3
- save section of first man page to history (#208738)
- remove dot from summary

* Fri Jan 19 2007 Miroslav Lichvar <mlichvar@redhat.com> 0.6.9-2
- use correct group when dropping group privileges (#221107)
- open also files without .info suffix
- make scriptlets safer
- make sure readline support isn't compiled in

* Tue Sep 12 2006 Miroslav Lichvar <mlichvar@redhat.com> 0.6.9-1.fc6
- update to 0.6.9
- package locale files

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.6.8-11.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.8-11.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.6.8-11.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Apr 22 2005 Mike A. Harris <mharris@redhat.com> 0.6.8-11
- Work around an idiotic bug in rpm (#118780) by using multiple Requires
  lines instead of the Requires(foo,bar) syntax that rpm documentation
  states is valid.  This fixes reported pinfo kickstart issue (#155700)

* Thu Mar  3 2005 Mike A. Harris <mharris@redhat.com> 0.6.8-10
- Rebuilt with gcc 4 for FC4
- Replaced Prereq: with Requires(post,preun)

* Thu Dec 23 2004 Mike A. Harris <mharris@redhat.com> 0.6.8-9
- Replaced pinfo-0.6.0-mkstemp.patch with updated pinfo-0.6.8-mkstemp.patch
  to fix an additional insecure tempnam() usage detected by our buildsystem

* Thu Dec 23 2004 Mike A. Harris <mharris@redhat.com> 0.6.8-8
- Added pinfo-0.6.8.memcorruption.patch and pinfo-0.6.8.memleak.patch by
  Sami Farin to fix a couple pinfo bugs reported in (#138770)

* Sun Sep 26 2004 Rik van Riel <riel@redhat.com> 0.6.8-7
- use htmlviewer as the browser, since lynx might not be installed (bz #123349)

* Wed Sep 22 2004 Mike A. Harris <mharris@redhat.com> 0.6.8-6
- Bump release and rebuild in rawhide for FC3

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jan 10 2004 Mike A. Harris <mharris@redhat.com> 0.6.8-3
- Added RPM_OPT_FLAGS to CFLAGS as it wasn't being used (#109197)

* Fri Oct 31 2003 Mike A. Harris <mharris@redhat.com> 0.6.8-2
- Updated package URL to current project homepage (#101214)

* Sat Oct 25 2003 Florian La Roche <Florian.LaRoche@redhat.de> 0.6.8-1
- Updated to 0.6.8

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May 18 2003 Mike A. Harris <mharris@redhat.com> 0.6.7-1
- Updated to 0.6.7
- Dropped already included patch pinfo-0.6.6-0.6.6p1.patch

* Wed Jan 22 2003 Mike A. Harris <mharris@redhat.com> 0.6.6-4
- Added pinfo-0.6.6-0.6.6p1.patch to fix bug (#78504)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Karsten Hopp <karsten@redhat.de> 0.6.6-2
- add missing Prereq

* Tue Nov 12 2002 Mike A. Harris <mharris@redhat.com> 0.6.6-1
- Updated to 0.6.6
- Corrected typos in description field

* Tue Nov 12 2002 Mike A. Harris <mharris@redhat.com> 0.6.4-9
- Now how ironic is *this* one?...  The info documentation on pinfo has been
  missing from our packages.  Mass rebuild tests caught this.  Fixed now.
- Added post/preun scripts for updating info dir db with install-info

* Sat Oct  5 2002 Mike A. Harris <mharris@redhat.com> 0.6.4-8
- All-arch rebuild
- Added _sysconfdir where appropriate

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.6.4-7
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com> 0.6.4-6
- automated rebuild

* Wed May 22 2002 Mike A. Harris <mharris@redhat.com> 0.6.4-5
- Bumped release to rebuild in rawhide

* Tue Feb 26 2002 Mike A. Harris <mharris@redhat.com> 0.6.4-4
- Bumped release to rebuild in rawhide

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 0.6.4-3
- automated rebuild

* Sun Dec 23 2001 Mike A. Harris <mharris@redhat.com> 0.6.4-2
- Bumped release to rebuild in rawhide

* Sun Dec 23 2001 Mike A. Harris <mharris@redhat.com> 0.6.4-1
- Updated to 0.6.4

* Wed Nov 21 2001 Mike A. Harris <mharris@redhat.com> 0.6.3-1
- Updated to 0.6.3

* Sat Jul 21 2001 Mike A. Harris <mharris@redhat.com> 0.6.1-2
- Add buildprereq on ncurses-devel

* Thu Jun 21 2001 Mike A. Harris <mharris@redhat.com> 0.6.1-1
- Updated to 0.6.1
- s/Copyright/License/ spec tag

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- move to the same group as the info and man packages

* Mon Aug  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- add pman(1) links, per documentation

* Wed Aug  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix possible crash due to use of tempnam()

* Wed Jul 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.6.0

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- spec file cleanups

* Thu Jun  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild for main distribution
- use %%makeinstall

* Wed May 17 2000 Tim Powers <timp@redhat.com>
- updated to 0.5.9
- use %%configure and %%{_prefix} where possible

* Mon Aug 30 1999 Tim Powers <timp@redhat.com>
- changed group

* Sun Aug 8 1999 Tim Powers <timp@redhat.com>
- rebuilt to be included in Powertools
