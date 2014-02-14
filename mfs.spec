# TODO:
# - check init scripts
Summary:	MooseFS - distributed, fault tolerant file system
Summary(pl.UTF-8):	MooseFS - rozproszony, odporny na awarie system plików
Name:		mfs
%define	ver	1.6.27
%define	subver	5
Version:	%{ver}.%{subver}
Release:	0.1
License:	GPL v3
Group:		Daemons
Source0:	http://www.moosefs.org/tl_files/mfscode/%{name}-%{ver}-%{subver}.tar.gz
# Source0-md5:	9eb1a2bde24b393aec3a1e4ced9fdd0f
Source1:	mfsmaster.init
Source2:	mfsmaster.sysconfig
Source3:	mfschunkserver.init
Source4:	mfschunkserver.sysconfig
Source5:	mfsmetalogger.init
Source6:	mfsmetalogger.sysconfig
Source7:	mfscgiserv.init
Source8:	mfscgiserv.sysconfig
URL:		http://www.moosefs.org/
BuildRequires:	libfuse-devel
BuildRequires:	pkgconfig
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mfsconfdir	%{_sysconfdir}/%{name}
%define		_localstatedir	/var/lib

%undefine 	__cxx

%description
MooseFS is an Open Source, easy to deploy and maintain, distributed,
fault tolerant file system for POSIX compliant OSes.

%description -l pl.UTF-8
MooseFS to mający otwarte źródła, łatwy we wdrożeniu i utrzymywaniu,
rozproszony i odporny na awarie system plików dla systemów
operacyjnych zgodnych z POSIX

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

%description chunkserver
MooseFS data server.

%description chunkserver -l pl.UTF-8
Serwer danych MooseFS.

%package client
Summary:	MooseFS client
Summary(pl.UTF-8):	Klient MooseFS
Group:		Daemons

%description client
MooseFS client: mfsmount and mfstools.

%description client -l pl.UTF-8
Klient MooseFS: mfsmount oraz mfstools.

%package cgi
Summary:	MooseFS CGI Monitor
Summary(pl.UTF-8):	Monitor CGI dla MooseFS-a
Group:		Daemons
Requires:	python-modules

%description cgi
MooseFS CGI Monitor.

%description cgi -l pl.UTF-8
Monitor CGI dla MooseFS-a.

%package cgiserv
Summary:	Simple CGI-capable HTTP server to run MooseFS CGI Monitor
Summary(pl.UTF-8):	Prosty serwer HTTP z obsługą CGI do uruchamiania Monitora CGI dla MooseFS-a
Group:		Daemons
Requires:	python
Requires:	python-modules

%description cgiserv
Simple CGI-capable HTTP server to run MooseFS CGI Monitor.

%description cgiserv -l pl.UTF-8
Prosty serwer HTTP z obsługą CGI do uruchamiania Monitora CGI dla
MooseFS-a.

%prep
%setup -q -n %{name}-%{ver}

%build
%configure \
	--with-default-user=mfs \
	--with-default-group=mfs

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

for i in $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/*.dist; do
	mv $i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/`basename $i .dist`;
done

install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig}
for f in %{SOURCE1} %{SOURCE3} %{SOURCE5} %{SOURCE7} ; do
	cp -p "$f" $RPM_BUILD_ROOT/etc/rc.d/init.d/$(basename $f .init)
done
for f in %{SOURCE2} %{SOURCE4} %{SOURCE6} %{SOURCE8} ; do
	cp -p "$f" $RPM_BUILD_ROOT/etc/sysconfig/$(basename $f .sysconfig)
done

%{__sed} -i -e '1s,/usr/bin/env python,/usr/bin/python,' $RPM_BUILD_ROOT%{_datadir}/mfscgi/*.cgi

%clean
rm -rf $RPM_BUILD_ROOT

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

%files master
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfsmaster
%attr(755,root,root) %{_sbindir}/mfsmetadump
%attr(755,root,root) %{_sbindir}/mfsmetarestore
%{_mandir}/man5/mfsexports.cfg.5*
%{_mandir}/man5/mfstopology.cfg.5*
%{_mandir}/man5/mfsmaster.cfg.5*
%{_mandir}/man8/mfsmaster.8*
%{_mandir}/man8/mfsmetarestore.8*
%dir %{mfsconfdir}
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsexports.cfg
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfstopology.cfg
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsmaster.cfg
%attr(750,mfs,mfs) %dir %{_localstatedir}/mfs
%attr(640,mfs,mfs) %{_localstatedir}/mfs/metadata.mfs.empty
%attr(754,root,root) /etc/rc.d/init.d/mfsmaster
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mfsmaster

%files metalogger
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfsmetalogger
%{_mandir}/man5/mfsmetalogger.cfg.5*
%{_mandir}/man8/mfsmetalogger.8*
%dir %{mfsconfdir}
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsmetalogger.cfg
%attr(750,mfs,mfs) %dir %{_localstatedir}/mfs
%attr(754,root,root) /etc/rc.d/init.d/mfsmetalogger
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mfsmetalogger

%files chunkserver
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfschunkserver
%{_mandir}/man5/mfschunkserver.cfg.5*
%{_mandir}/man5/mfshdd.cfg.5*
%{_mandir}/man8/mfschunkserver.8*
%dir %{mfsconfdir}
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfschunkserver.cfg
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfshdd.cfg
%attr(750,mfs,mfs) %dir %{_localstatedir}/mfs
%attr(754,root,root) /etc/rc.d/init.d/mfschunkserver
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mfschunkserver

%files client
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_bindir}/mfsappendchunks
%attr(755,root,root) %{_bindir}/mfscheckfile
%attr(755,root,root) %{_bindir}/mfsdeleattr
%attr(755,root,root) %{_bindir}/mfsdirinfo
%attr(755,root,root) %{_bindir}/mfsfileinfo
%attr(755,root,root) %{_bindir}/mfsfilerepair
%attr(755,root,root) %{_bindir}/mfsgeteattr
%attr(755,root,root) %{_bindir}/mfsgetgoal
%attr(755,root,root) %{_bindir}/mfsgettrashtime
%attr(755,root,root) %{_bindir}/mfsmakesnapshot
%attr(755,root,root) %{_bindir}/mfsmount
%attr(755,root,root) %{_bindir}/mfsrgetgoal
%attr(755,root,root) %{_bindir}/mfsrgettrashtime
%attr(755,root,root) %{_bindir}/mfsrsetgoal
%attr(755,root,root) %{_bindir}/mfsrsettrashtime
%attr(755,root,root) %{_bindir}/mfsseteattr
%attr(755,root,root) %{_bindir}/mfssetgoal
%attr(755,root,root) %{_bindir}/mfssettrashtime
%attr(755,root,root) %{_bindir}/mfssnapshot
%attr(755,root,root) %{_bindir}/mfstools
%{_mandir}/man1/mfsappendchunks.1*
%{_mandir}/man1/mfscheckfile.1*
%{_mandir}/man1/mfsdeleattr.1*
%{_mandir}/man1/mfsdirinfo.1*
%{_mandir}/man1/mfsfileinfo.1*
%{_mandir}/man1/mfsfilerepair.1*
%{_mandir}/man1/mfsgeteattr.1*
%{_mandir}/man1/mfsgetgoal.1*
%{_mandir}/man1/mfsgettrashtime.1*
%{_mandir}/man1/mfsmakesnapshot.1*
%{_mandir}/man1/mfsrgetgoal.1*
%{_mandir}/man1/mfsrgettrashtime.1*
%{_mandir}/man1/mfsrsetgoal.1*
%{_mandir}/man1/mfsrsettrashtime.1*
%{_mandir}/man1/mfsseteattr.1*
%{_mandir}/man1/mfssetgoal.1*
%{_mandir}/man1/mfssettrashtime.1*
%{_mandir}/man1/mfstools.1*
%{_mandir}/man7/mfs.7*
%{_mandir}/man7/moosefs.7*
%{_mandir}/man8/mfsmount.8*
%dir %{mfsconfdir}
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsmount.cfg

%files cgi
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%dir %{_datadir}/mfscgi
%attr(755,root,root) %{_datadir}/mfscgi/chart.cgi
%attr(755,root,root) %{_datadir}/mfscgi/mfs.cgi
%{_datadir}/mfscgi/err.gif
%{_datadir}/mfscgi/favicon.ico
%{_datadir}/mfscgi/index.html
%{_datadir}/mfscgi/logomini.png
%{_datadir}/mfscgi/mfs.css

%files cgiserv
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/mfscgiserv
%{_mandir}/man8/mfscgiserv.8*
%attr(754,root,root) /etc/rc.d/init.d/mfscgiserv
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/mfscgiserv
