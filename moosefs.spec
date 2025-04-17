# TODO:
# - rename init scripts following upstream, check consistency with upstream-provided ones
# - check init scripts
Summary:	MooseFS - distributed, fault tolerant file system
Summary(pl.UTF-8):	MooseFS - rozproszony, odporny na awarie system plików
Name:		moosefs
Version:	4.57.6
Release:	0.1
License:	GPL v2
Group:		Daemons
#Source0Download: https://github.com/moosefs/moosefs/releases
Source0:	https://github.com/moosefs/moosefs/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	86a86a651c361dbd462054105141a49e
Source1:	mfsmaster.init
Source2:	mfsmaster.sysconfig
Source3:	mfschunkserver.init
Source4:	mfschunkserver.sysconfig
Source5:	mfsmetalogger.init
Source6:	mfsmetalogger.sysconfig
Source7:	mfscgiserv.init
Source8:	mfscgiserv.sysconfig
URL:		https://moosefs.com/
BuildRequires:	libfuse3-devel >= 3.2.1
BuildRequires:	libpcap-devel
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	rpm-pythonprov
BuildRequires:	zlib-devel
Obsoletes:	mfs < 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mfsconfdir	%{_sysconfdir}/mfs
%define		_localstatedir	/var/lib

%undefine 	__cxx

%description
MooseFS is an Open Source, easy to deploy and maintain, distributed,
fault tolerant file system for POSIX compliant OSes.

%description -l pl.UTF-8
MooseFS to mający otwarte źródła, łatwy we wdrożeniu i utrzymywaniu,
rozproszony i odporny na awarie system plików dla systemów
operacyjnych zgodnych z POSIX

%package libs
Summary:	MooseFS I/O client library
Summary(pl.UTF-8):	Biblioteka kliencka we/wy MooseFS
Group:		Libraries

%description libs
MooseFS I/O client library.

%description libs -l pl.UTF-8
Biblioteka kliencka we/wy MooseFS.

%package devel
Summary:	Header files for MooseFS I/O client library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki klienckiej we/wy MooseFS
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for MooseFS I/O client library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki klienckiej we/wy MooseFS.

%package static
Summary:	Static MooseFS I/O client library
Summary(pl.UTF-8):	Statyczna biblioteka kliencka we/wy MooseFS
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MooseFS I/O client library.

%description static -l pl.UTF-8
Statyczna biblioteka kliencka we/wy MooseFS.

%package master
Summary:	MooseFS master server
Summary(pl.UTF-8):	Serwer zarządzający MooseFS
Group:		Daemons
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	group(mfs)
Provides:	user(mfs)
Obsoletes:	mfs-master < 2

%description master
MooseFS master (metadata) server together with metarestore utility.

%description master -l pl.UTF-8
Serwer zarządzający (metadanych) MooseFS wraz z narzędziem
metarestore.

%package metalogger
Summary:	MooseFS metalogger server
Summary(pl.UTF-8):	Serwer metaloggera MooseFS
Group:		Daemons
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	group(mfs)
Provides:	user(mfs)
Obsoletes:	mfs-metalogger < 2

%description metalogger
MooseFS metalogger (metadata replication) server.

%description metalogger -l pl.UTF-8
Serwer metaloggera (replikacji metadanych) MooseFS.

%package chunkserver
Summary:	MooseFS data server
Summary(pl.UTF-8):	Serwer danych MooseFS
Group:		Daemons
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Provides:	group(mfs)
Provides:	user(mfs)
Obsoletes:	mfs-chunkserver < 2

%description chunkserver
MooseFS data server.

%description chunkserver -l pl.UTF-8
Serwer danych MooseFS.

%package client
Summary:	MooseFS client
Summary(pl.UTF-8):	Klient MooseFS
Group:		Daemons
# only for mfsbdev currently
Requires:	%{name}-libs = %{version}-%{release}
# for mfsmount
Requires:	libfuse3 >= 3.2.1
Obsoletes:	mfs-client < 2

%description client
MooseFS client: mfsmount and mfstools.

%description client -l pl.UTF-8
Klient MooseFS: mfsmount oraz mfstools.

%package cgi
Summary:	MooseFS CGI Monitor
Summary(pl.UTF-8):	Monitor CGI dla MooseFS-a
Group:		Daemons
Requires:	python-modules
Obsoletes:	mfs-cgi < 2

%description cgi
MooseFS CGI Monitor.

%description cgi -l pl.UTF-8
Monitor CGI dla MooseFS-a.

%package cgiserv
Summary:	Simple CGI-capable HTTP server to run MooseFS CGI Monitor
Summary(pl.UTF-8):	Prosty serwer HTTP z obsługą CGI do uruchamiania Monitora CGI dla MooseFS-a
Group:		Daemons
Requires:	python3 >= 1:3.4
Requires:	python3-modules >= 1:3.4
Obsoletes:	mfs-cgiserv < 2

%description cgiserv
Simple CGI-capable HTTP server to run MooseFS CGI Monitor.

%description cgiserv -l pl.UTF-8
Prosty serwer HTTP z obsługą CGI do uruchamiania Monitora CGI dla
MooseFS-a.

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env @PYTHON@,%{__python3},' mfsscripts/mfs*.py.in mfsscripts/*.cgi.in

# nothing bash-specific inside
%{__sed} -i -e '1s,/usr/bin/env bash,/bin/sh,' \
	mfsclient/{mfsgetgoal,mfssetgoal,mfscopygoal} \
	mfsmaster/mfsmetarestore

%build
%configure \
	--disable-silent-rules \
	--with-default-user=mfs \
	--with-default-group=mfs \
	--with-systemdsystemunitdir=%{systemdunitdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no external dependencies
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmfsio.la

for i in $RPM_BUILD_ROOT%{mfsconfdir}/*.sample; do
	%{__mv} $i $RPM_BUILD_ROOT%{mfsconfdir}/`basename $i .sample`;
done

install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig}
for f in %{SOURCE1} %{SOURCE3} %{SOURCE5} %{SOURCE7} ; do
	cp -p "$f" $RPM_BUILD_ROOT/etc/rc.d/init.d/$(basename $f .init)
done
for f in %{SOURCE2} %{SOURCE4} %{SOURCE6} %{SOURCE8} ; do
	cp -p "$f" $RPM_BUILD_ROOT/etc/sysconfig/$(basename $f .sysconfig)
done

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%pre master
%groupadd -g 282 mfs
%useradd -u 282 -d /var/lib/mfs -s /bin/false -c "MooseFS pseudo user" -g mfs mfs

%postun master
if [ "$1" = "0" ]; then
	%userremove mfs
	%groupremove mfs
fi

%pre metalogger
%groupadd -g 282 mfs
%useradd -u 282 -d /var/lib/mfs -s /bin/false -c "MooseFS pseudo user" -g mfs mfs

%postun metalogger
if [ "$1" = "0" ]; then
	%userremove mfs
	%groupremove mfs
fi

%pre chunkserver
%groupadd -g 282 mfs
%useradd -u 282 -d /var/lib/mfs -s /bin/false -c "MooseFS pseudo user" -g mfs mfs

%postun chunkserver
if [ "$1" = "0" ]; then
	%userremove mfs
	%groupremove mfs
fi

%files libs
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_libdir}/libmfsio.so.*.*.*
%ghost %{_libdir}/libmfsio.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libmfsio.so
%{_includedir}/mfsio.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libmfsio.a

%files master
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_sbindir}/mfsmaster
%attr(755,root,root) %{_sbindir}/mfsmetadirinfo
%attr(755,root,root) %{_sbindir}/mfsmetadump
%attr(755,root,root) %{_sbindir}/mfsmetarestore
%attr(755,root,root) %{_sbindir}/mfsmetasearch
%attr(755,root,root) %{_sbindir}/mfsstatsdump
%attr(755,root,root) %{_sbindir}/mfssupervisor
%{_mandir}/man5/mfsexports.cfg.5*
%{_mandir}/man5/mfsipmap.cfg.5*
%{_mandir}/man5/mfstopology.cfg.5*
%{_mandir}/man5/mfsmaster.cfg.5*
%{_mandir}/man8/mfsmaster.8*
%{_mandir}/man8/mfsmetadirinfo.8*
%{_mandir}/man8/mfsmetadump.8*
%{_mandir}/man8/mfsmetarestore.8*
%{_mandir}/man8/mfsmetasearch.8*
%{_mandir}/man8/mfsstatsdump.8*
%{_mandir}/man8/mfssupervisor.8*
%dir %{mfsconfdir}
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsexports.cfg
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsipmap.cfg
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsmaster.cfg
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfstopology.cfg
%attr(750,mfs,mfs) %dir %{_localstatedir}/mfs
%attr(640,mfs,mfs) %{_localstatedir}/mfs/metadata.mfs.empty
%attr(754,root,root) /etc/rc.d/init.d/mfsmaster
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mfsmaster
%{systemdunitdir}/moosefs-master.service
%{systemdunitdir}/moosefs-master@.service

%files metalogger
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_sbindir}/mfsmetalogger
%{_mandir}/man5/mfsmetalogger.cfg.5*
%{_mandir}/man8/mfsmetalogger.8*
%dir %{mfsconfdir}
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsmetalogger.cfg
%attr(750,mfs,mfs) %dir %{_localstatedir}/mfs
%attr(754,root,root) /etc/rc.d/init.d/mfsmetalogger
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mfsmetalogger
%{systemdunitdir}/moosefs-metalogger.service
%{systemdunitdir}/moosefs-metalogger@.service

%files chunkserver
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_sbindir}/mfschunkdbdump
%attr(755,root,root) %{_sbindir}/mfschunkserver
%attr(755,root,root) %{_sbindir}/mfschunktool
%attr(755,root,root) %{_sbindir}/mfscsstatsdump
%{_mandir}/man5/mfschunkserver.cfg.5*
%{_mandir}/man5/mfshdd.cfg.5*
%{_mandir}/man8/mfschunkdbdump.8*
%{_mandir}/man8/mfschunkserver.8*
%{_mandir}/man8/mfschunktool.8*
%{_mandir}/man8/mfscsstatsdump.8*
%dir %{mfsconfdir}
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfschunkserver.cfg
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfshdd.cfg
%attr(750,mfs,mfs) %dir %{_localstatedir}/mfs
%attr(754,root,root) /etc/rc.d/init.d/mfschunkserver
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mfschunkserver
%{systemdunitdir}/moosefs-chunkserver.service
%{systemdunitdir}/moosefs-chunkserver@.service

%files client
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) /sbin/mount.moosefs
%attr(755,root,root) %{_bindir}/mfsappendchunks
%attr(755,root,root) %{_bindir}/mfsarchive
%attr(755,root,root) %{_bindir}/mfscheckfile
%attr(755,root,root) %{_bindir}/mfschkarchive
%attr(755,root,root) %{_bindir}/mfscli
%attr(755,root,root) %{_bindir}/mfsclonesclass
%attr(755,root,root) %{_bindir}/mfsclrarchive
%attr(755,root,root) %{_bindir}/mfscopyeattr
%attr(755,root,root) %{_bindir}/mfscopygoal
%attr(755,root,root) %{_bindir}/mfscopyquota
%attr(755,root,root) %{_bindir}/mfscopysclass
%attr(755,root,root) %{_bindir}/mfscopytrashretention
%attr(755,root,root) %{_bindir}/mfscopytrashtime
%attr(755,root,root) %{_bindir}/mfscreatepattern
%attr(755,root,root) %{_bindir}/mfscreatesclass
%attr(755,root,root) %{_bindir}/mfsdeleattr
%attr(755,root,root) %{_bindir}/mfsdeletepattern
%attr(755,root,root) %{_bindir}/mfsdeletesclass
%attr(755,root,root) %{_bindir}/mfsdelquota
%attr(755,root,root) %{_bindir}/mfsdiagtools
%attr(755,root,root) %{_bindir}/mfsdirinfo
%attr(755,root,root) %{_bindir}/mfseattr
%attr(755,root,root) %{_bindir}/mfsfacl
%attr(755,root,root) %{_bindir}/mfsfileinfo
%attr(755,root,root) %{_bindir}/mfsfilepaths
%attr(755,root,root) %{_bindir}/mfsfilerepair
%attr(755,root,root) %{_bindir}/mfsgeteattr
%attr(755,root,root) %{_bindir}/mfsgetfacl
%attr(755,root,root) %{_bindir}/mfsgetgoal
%attr(755,root,root) %{_bindir}/mfsgetquota
%attr(755,root,root) %{_bindir}/mfsgetsclass
%attr(755,root,root) %{_bindir}/mfsgettrashretention
%attr(755,root,root) %{_bindir}/mfsgettrashtime
%attr(755,root,root) %{_bindir}/mfsimportsclass
%attr(755,root,root) %{_bindir}/mfslistpattern
%attr(755,root,root) %{_bindir}/mfslistsclass
%attr(755,root,root) %{_bindir}/mfsmakesnapshot
%attr(755,root,root) %{_bindir}/mfsmodifysclass
%attr(755,root,root) %{_bindir}/mfsmount
%attr(755,root,root) %{_bindir}/mfspatadmin
%attr(755,root,root) %{_bindir}/mfsquota
%attr(755,root,root) %{_bindir}/mfsrenamesclass
%attr(755,root,root) %{_bindir}/mfsrmsnapshot
%attr(755,root,root) %{_bindir}/mfsscadmin
%attr(755,root,root) %{_bindir}/mfssclass
%attr(755,root,root) %{_bindir}/mfssetarchive
%attr(755,root,root) %{_bindir}/mfsseteattr
%attr(755,root,root) %{_bindir}/mfssetfacl
%attr(755,root,root) %{_bindir}/mfssetgoal
%attr(755,root,root) %{_bindir}/mfssetquota
%attr(755,root,root) %{_bindir}/mfssetsclass
%attr(755,root,root) %{_bindir}/mfssettrashretention
%attr(755,root,root) %{_bindir}/mfssettrashtime
%attr(755,root,root) %{_bindir}/mfssnapshots
%attr(755,root,root) %{_bindir}/mfstrashretention
%attr(755,root,root) %{_bindir}/mfstrashtime
%attr(755,root,root) %{_bindir}/mfstrashtool
%attr(755,root,root) %{_bindir}/mfsxchgsclass
%attr(755,root,root) %{_sbindir}/mfsbdev
%attr(755,root,root) %{_sbindir}/mfsnetdump
%{_mandir}/man1/mfsappendchunks.1*
%{_mandir}/man1/mfsarchive.1*
%{_mandir}/man1/mfscheckfile.1*
%{_mandir}/man1/mfschkarchive.1*
%{_mandir}/man1/mfscli.1*
%{_mandir}/man1/mfsclonesclass.1*
%{_mandir}/man1/mfsclrarchive.1*
%{_mandir}/man1/mfscopyeattr.1*
%{_mandir}/man1/mfscopygoal.1*
%{_mandir}/man1/mfscopyquota.1*
%{_mandir}/man1/mfscopysclass.1*
%{_mandir}/man1/mfscopytrashretention.1*
%{_mandir}/man1/mfscopytrashtime.1*
%{_mandir}/man1/mfscreatepattern.1*
%{_mandir}/man1/mfscreatesclass.1*
%{_mandir}/man1/mfsdeleattr.1*
%{_mandir}/man1/mfsdeletepattern.1*
%{_mandir}/man1/mfsdeletesclass.1*
%{_mandir}/man1/mfsdelquota.1*
%{_mandir}/man1/mfsdiagtools.1*
%{_mandir}/man1/mfsdirinfo.1*
%{_mandir}/man1/mfseattr.1*
%{_mandir}/man1/mfsfacl.1*
%{_mandir}/man1/mfsfileinfo.1*
%{_mandir}/man1/mfsfilepaths.1*
%{_mandir}/man1/mfsfilerepair.1*
%{_mandir}/man1/mfsgeteattr.1*
%{_mandir}/man1/mfsgetfacl.1*
%{_mandir}/man1/mfsgetgoal.1*
%{_mandir}/man1/mfsgetquota.1*
%{_mandir}/man1/mfsgetsclass.1*
%{_mandir}/man1/mfsgettrashretention.1*
%{_mandir}/man1/mfsgettrashtime.1*
%{_mandir}/man1/mfsgoal.1*
%{_mandir}/man1/mfsimportsclass.1*
%{_mandir}/man1/mfslistpattern.1*
%{_mandir}/man1/mfslistsclass.1*
%{_mandir}/man1/mfsmakesnapshot.1*
%{_mandir}/man1/mfsmodifysclass.1*
%{_mandir}/man1/mfspatadmin.1*
%{_mandir}/man1/mfsquota.1*
%{_mandir}/man1/mfsrenamesclass.1*
%{_mandir}/man1/mfsrmsnapshot.1*
%{_mandir}/man1/mfsscadmin.1*
%{_mandir}/man1/mfssclass.1*
%{_mandir}/man1/mfssetarchive.1*
%{_mandir}/man1/mfsseteattr.1*
%{_mandir}/man1/mfssetfacl.1*
%{_mandir}/man1/mfssetgoal.1*
%{_mandir}/man1/mfssetquota.1*
%{_mandir}/man1/mfssetsclass.1*
%{_mandir}/man1/mfssettrashretention.1*
%{_mandir}/man1/mfssettrashtime.1*
%{_mandir}/man1/mfssnapshots.1*
%{_mandir}/man1/mfstools.1*
%{_mandir}/man1/mfstrashretention.1*
%{_mandir}/man1/mfstrashtime.1*
%{_mandir}/man1/mfsxchgsclass.1*
%{_mandir}/man5/mfsbdev.cfg.5*
%{_mandir}/man5/mfsmount.cfg.5*
%{_mandir}/man7/moosefs.7*
%{_mandir}/man8/mfsbdev.8*
%{_mandir}/man8/mfsmount.8*
%{_mandir}/man8/mfsnetdump.8*
%{_mandir}/man8/mount.moosefs.8*
%dir %{mfsconfdir}
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsmount.cfg

%files cgi
%defattr(644,root,root,755)
%doc NEWS README
%dir %{_datadir}/mfscgi
%attr(755,root,root) %{_datadir}/mfscgi/chart.cgi
%attr(755,root,root) %{_datadir}/mfscgi/chartdata.cgi
%attr(755,root,root) %{_datadir}/mfscgi/mfs.cgi
%{_datadir}/mfscgi/mfsgraph.py
%{_datadir}/mfscgi/err.gif
%{_datadir}/mfscgi/favicon.ico
%{_datadir}/mfscgi/index.html
%{_datadir}/mfscgi/mfs.css
%{_datadir}/mfscgi/logo*.svg
%{_datadir}/mfscgi/*.js

%files cgiserv
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mfscgiserv
%{_mandir}/man8/mfscgiserv.8*
%attr(754,root,root) /etc/rc.d/init.d/mfscgiserv
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mfscgiserv
%{systemdunitdir}/moosefs-cgiserv.service
