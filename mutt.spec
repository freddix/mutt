Summary:	The Mutt Mail User Agent
Name:		mutt
Version:	1.5.22
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	ftp://ftp.mutt.org/mutt/devel/%{name}-%{version}.tar.gz
# Source0-md5:	48267aba1bc53db636777f4a1ec87cb6
Patch0:		%{name}-manual.patch
Patch1:		%{name}-Muttrc_mbox_path.patch
Patch2:		%{name}-po.patch
Patch3:		%{name}-forcedotlock.patch
Patch4:		%{name}-gpgme.patch
URL:		http://www.mutt.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	db-devel
BuildRequires:	gettext-devel
BuildRequires:	gpgme-devel
BuildRequires:	libidn-devel
BuildRequires:	libsasl2-devel
BuildRequires:	libxslt-progs
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
Requires:	iconv
Suggests:	mailcap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mutt is a small but very poweful full-screen Unix mail client.
Features include MIME support, color, POP3 support, message threading,
bindable keys, and threaded sorting mode.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{__sed} -i "s|AM_C_PROTOTYPES||" configure.ac

%build
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gpgme				\
	--enable-hcache				\
	--enable-imap				\
	--enable-mailtool			\
	--enable-pop				\
	--enable-smtp				\
	--with-bdb=/usr				\
	--with-curses				\
	--with-docdir=%{_docdir}/%{name}	\
	--with-mailpath=/var/mail 		\
	--with-mixmaster			\
	--with-regex				\
	--with-sasl				\
	--with-ssl				\
	--without-gdbm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT	\
	DOTLOCK_GROUP=

# keep manual.txt.gz, the rest is installed as %doc
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}/[!m]*

rm -f $RPM_BUILD_ROOT%{_mandir}/man5/mbox.5*
rm -f $RPM_BUILD_ROOT/etc/mime.types

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc contrib/{*rc*,*cap*} ChangeLog README TODO NEWS README.SECURITY README.SSL
%config(noreplace,missingok) %verify(not md5 size mtime) %{_sysconfdir}/Muttrc
%attr(755,root,root) %{_bindir}/mutt
%attr(755,root,root) %{_bindir}/flea
%attr(755,root,root) %{_bindir}/muttbug
%attr(755,root,root) %{_bindir}/pgp*
%attr(755,root,root) %{_bindir}/smime_keys
%attr(2755,root,mail) %{_bindir}/mutt_dotlock
%{_docdir}/%{name}
%{_mandir}/man*/*

