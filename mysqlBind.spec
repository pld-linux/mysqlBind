Summary:	An ISP quality, browser-based DNS/BIND name server manager
Name:		mysqlBind
Version:	1.8
Release:	0.5
License:	GPL v2
Group:		-
Source0:	http://openisp.net/%{name}/%{name}%{version}.tar.gz
# Source0-md5:	1b360bdc74bf4d21998256fa09d45af7
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-mysql_user.patch
URL:		http://openisp.net/mysqlBind/
BuildRequires:	mysql-devel
#PreReq:		-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
Requires:	mysql
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir %{_libdir}/%{name}

%description
myqslBind manages multiple DNS/BIND (8 and 9) name servers. It automates
updates to multiple DNS servers, centralizes and stores all zone and
resource records for sets of related name servers
(ns0...nsN.yourisp.net), and even manages different name server sets
from a single browser-based interface. Unlimited master and slave name
servers update their zone information via a job queue system that uses
MySQL socket connections. Advanced operations can use mySQL replication
clusters for high availability and redundancy. Large ISPs and other
organizations should note that they can easily add SQL functions to
customize the program for their special needs. It supports
authentication via SSL Unix password login, SSL personal certificate, or
IP-based access with multiple permission levels and individual record
ownership. It is also compatible with mysqlISP.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CFLAGS="-Wall -DLinux %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_appdir},/var/lib/%{name}/{data,docs}}

%{__make} install \
	CGIDIR=$RPM_BUILD_ROOT%{_appdir}/

install data/* $RPM_BUILD_ROOT/var/lib/%{name}/data
install docs/* $RPM_BUILD_ROOT/var/lib/%{name}/docs

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post

%preun

%postun

%files
%defattr(644,root,root,755)
%doc CHANGES INSTALL
%dir %{_appdir}
%attr(755,root,root) %{_appdir}/*
/var/lib/%{name}
