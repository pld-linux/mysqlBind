Summary:	An ISP quality, browser-based DNS/BIND name server manager
Name:		mysqlBind
Version:	1.8
Release:	0.6
License:	GPL v2
Group:		Networking/Admin
Source0:	http://openisp.net/%{name}/%{name}%{version}.tar.gz
# Source0-md5:	1b360bdc74bf4d21998256fa09d45af7
Source1:	%{name}.conf
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-mysql_user.patch
Patch2:		%{name}-paths.patch
URL:		http://openisp.net/mysqlBind/
BuildRequires:	mysql-devel
#PreReq:		-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
Requires:	apache-mod_ss;
Requires:	bind-utils
Requires:	mysql
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
%patch2 -p1

%build
%{__make} \
	CFLAGS="-Wall -DLinux %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/httpd,%{_appdir},/var/lib/%{name}/data}

%{__make} install \
	CGIDIR=$RPM_BUILD_ROOT%{_appdir}/

install data/* $RPM_BUILD_ROOT/var/lib/%{name}/data
install docs/tutorial.html $RPM_BUILD_ROOT%{_appdir}/mysqlbind.tutorial.txt

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*mysqlBind.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/mysqlBind.conf" >> /etc/httpd/httpd.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi
		
%preun
if [ "$1" = "0" ]; then
	umask 027
	grep -v "^Include.*mysqlBind.conf" /etc/httpd/httpd.conf > \
		/etc/httpd/httpd.conf.tmp
	mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc CHANGES INSTALL
%config(noreplace) %verify(not md5 size mtime) /etc/httpd/%{name}.conf
%dir %{_appdir}
%attr(755,root,root) %{_appdir}/*.cgi
%{_appdir}/*.txt
/var/lib/%{name}/data
