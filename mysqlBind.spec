Summary:	An ISP quality, browser-based DNS/BIND name server manager
Summary(pl.UTF-8):	Oparty na przeglądarce rozbudowany zarządca serwerów DNS/BIND
Name:		mysqlBind
Version:	1.94
Release:	0.5
License:	GPL v2
Group:		Networking/Admin
Source0:	http://openisp.net/mysqlBind/%{name}%{version}.tar.gz
# Source0-md5:	aea27dd7a641d6c4d9d68e216e8650fb
Source1:	%{name}.conf
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-CC.patch
URL:		http://openisp.net/mysqlBind/
BuildRequires:	mysql-devel
Requires:	apache >= 2.0
Requires:	apache-mod_ssl
Requires:	bind
Requires:	bind-utils
Requires:	mysql
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir %{_libdir}/%{name}

%description
mysqlBind manages multiple DNS/BIND (8 and 9) name servers. It automates
updates to multiple DNS servers, centralizes and stores all zone and
resource records for sets of related name servers
(ns0...nsN.yourisp.net), and even manages different name server sets
from a single browser-based interface. Unlimited master and slave name
servers update their zone information via a job queue system that uses
MySQL socket connections. Advanced operations can use MySQL replication
clusters for high availability and redundancy. Large ISPs and other
organizations should note that they can easily add SQL functions to
customize the program for their special needs. It supports
authentication via SSL Unix password login, SSL personal certificate, or
IP-based access with multiple permission levels and individual record
ownership. It is also compatible with mysqlISP.

%description -l pl.UTF-8
mysqlBind zarządza wieloma serwerami nazw DNS/BIND (8 i 9).
Automatyzuje uaktualnienia wielu serwerów DNS, centralizuje i
przechowuje wszystkie rekordy stref i zasobów dla zbiorów powiązanych
serwerów nazw (ns0...nsN.twojisp.net), a nawet zarządza różnymi
zbiorami serwerów nazw z jednego interfejsu opartego na przeglądarce.
Nieograniczona liczba serwerów głównych i zapasowych uaktualnia swoje
informacje o strefach poprzez system kolejkowania zadań używający
połączeń przez gniazda MySQL. Zaawansowane operacje mogą używać
klastrów replikacyjnych MySQL-a dla wysokiej dostępności i
redundancji. Duzi ISP i inne organizacje powinni zauważyć, jak łatwo
można dodać funkcje SQL aby dostosować program do własnych,
specjalnych potrzeb. Program obsługuje uwierzytelnienie przez
logowanie hasłem po SSL, certyfikat osobisty SSL lub dostęp oparty o
IP z wieloma stopniami uprawnień i indywidualną własnością rekordów.
Jest także kompatybilny z mysqlISP.

%prep
%setup -q -n %{name}%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
echo '
#define LIBDIR "/usr/lib"
#define NAMED_CONF "/var/lib/named/etc"
' >> local.h

%{__make} \
	CC="%{__cc}" \
	CFLAGS="-Wall -DLinux %{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/httpd,%{_appdir}/{data,setup9}} \

%{__make} install \
	CGIDIR=$RPM_BUILD_ROOT%{_appdir}/

install data/* $RPM_BUILD_ROOT%{_appdir}/data
install setup9/* $RPM_BUILD_ROOT%{_appdir}/setup9
install docs/tutorial.html $RPM_BUILD_ROOT%{_appdir}/mysqlbind.tutorial.txt

for i in `seq 0 9` a b c d e f g h i j k l m n o p q r s t u v w x y z; do
	install -d $RPM_BUILD_ROOT/var/lib/named/etc/named.d/master/$i
	install -d $RPM_BUILD_ROOT/var/lib/named/etc/named.d/slave/$i
done

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
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
%dir %{_appdir}
%attr(755,root,root) %{_appdir}/*.cgi
%{_appdir}/*.txt
%{_appdir}/data
%{_appdir}/setup9
/var/lib/named/etc/named.d
