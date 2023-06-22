# TODO:
# - init script/systemd support
# - PLDify configuration more
# (it's based mainly on gdm 2.x)
#
# Conditional build:
%bcond_without	selinux		# SELinux support

%define		glib2_ver	1:2.56.0
Summary:	GNOME Display Manager
Summary(es.UTF-8):	Administrador de Entrada del GNOME
Summary(ja.UTF-8):	GNOME ディスプレイマネージャ
Summary(pl.UTF-8):	gdm - zarządca ekranów GNOME
Summary(pt_BR.UTF-8):	Gerenciador de Entrada do GNOME
Summary(ru.UTF-8):	Дисплейный менеджер GNOME
Summary(uk.UTF-8):	Дисплейний менеджер GNOME
Name:		mdm
Version:	2.0.19
Release:	1
License:	GPL v2+
Group:		X11/Applications
#Source0Download: https://github.com/linuxmint/mdm/tags
Source0:	https://github.com/linuxmint/mdm/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d4b25154f5ea741cd04939c24606622c
Patch0:		%{name}-format.patch
Patch1:		%{name}-pixmapdir.patch
Patch2:		%{name}-conf.patch
URL:		https://github.com/linuxmint/mdm
BuildRequires:	ConsoleKit-devel
%{?with_selinux:BuildRequires:	attr-devel}
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.78
BuildRequires:	gdk-pixbuf2-devel >= 2.22.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.37.3
BuildRequires:	gtk-webkit-devel >= 1.3.10
BuildRequires:	gtk+2-devel >= 2:2.24.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libart_lgpl-devel >= 2.3.17
BuildRequires:	libglade2-devel >= 2.0
BuildRequires:	libgnomecanvas-devel >= 2.11.1
BuildRequires:	librsvg-devel >= 2.14.4
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.7.4
BuildRequires:	pam-devel
BuildRequires:	pango-devel >= 1:1.14.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libdmx-devel
BuildRequires:	yelp-tools
Requires(post,postun):	gtk-update-icon-cache
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	hicolor-icon-theme
Provides:	XDM
Provides:	group(xdm)
Provides:	user(xdm)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localstatedir	/var/lib

%description
MDM (MDM Display Manager) is X display manager based on GDM.

%description -l pl.UTF-8
MDM (MDM Display Manager) to zarządca ekranów X oparty na GDM.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' files/usr/bin/{mdm-recovery,mdm-theme-emulator}
%{__sed} -i -e '1s,/usr/bin/python$,%{__python},' files/usr/bin/mdm-unlock-logind

%{__sed} -i '/^po\/Makefile\.in/d' configure.ac

%build
%{__gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	ZENITY=/usr/bin/zenity \
	--enable-authentication-scheme=pam \
	--disable-console-helper \
	--disable-compile-warnings \
	--enable-ipv6 \
	--enable-secureremote \
	--disable-static \
	--with-console-kit \
	--with-dmx \
	--with-libaudit \
	%{?with_selinux:--with-selinux} \
	--with-tcp-wrappers \
	--with-xinerama

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT/etc/security \
	$RPM_BUILD_ROOT%{_datadir}/mdm/html-themes

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la

touch $RPM_BUILD_ROOT/etc/security/blacklist.mdm

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{sr@Latn,sr@latin}

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 55 -r -f xdm
%useradd -u 55 -r -d /home/services/xdm -s /bin/false -c "X Display Manager" -g xdm xdm

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor
if [ "$1" = "0" ]; then
	%userremove xdm
	%groupremove xdm
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README TODO
%attr(755,root,root) %{_bindir}/mdm-dmx-reconnect-proxy
%attr(755,root,root) %{_bindir}/mdm-get-monitor-scale
%attr(755,root,root) %{_bindir}/mdm-recovery
%attr(755,root,root) %{_bindir}/mdm-set-keyboard-layout
%attr(755,root,root) %{_bindir}/mdm-theme-emulator
%attr(755,root,root) %{_bindir}/mdm-unlock-logind
%attr(755,root,root) %{_bindir}/mdmflexiserver
%attr(755,root,root) %{_sbindir}/mdm
%attr(755,root,root) %{_sbindir}/mdm-binary
%attr(755,root,root) %{_sbindir}/mdm-restart
%attr(755,root,root) %{_sbindir}/mdm-safe-restart
%attr(755,root,root) %{_sbindir}/mdm-stop
%attr(755,root,root) %{_sbindir}/mdmsetup
%attr(755,root,root) %{_libexecdir}/mdm-ssh-session
%attr(755,root,root) %{_libexecdir}/mdmaskpass
%attr(755,root,root) %{_libexecdir}/mdmgreeter
%attr(755,root,root) %{_libexecdir}/mdmlogin
%attr(755,root,root) %{_libexecdir}/mdmopen
%attr(755,root,root) %{_libexecdir}/mdmtranslate
%attr(755,root,root) %{_libexecdir}/mdmwebkit
%attr(755,root,root) %{_libdir}/gtk-2.0/modules/libdwellmouselistener.so
%attr(755,root,root) %{_libdir}/gtk-2.0/modules/libkeymouselistener.so
# where should this dir belong? is it handled in PLD?
%dir /etc/X11/Xsession.d
/etc/X11/Xsession.d/99mdm
%dir %{_sysconfdir}/mdm
%dir %{_sysconfdir}/mdm/Init
%attr(755,root,root) %config %{_sysconfdir}/mdm/Init/Default
%dir %{_sysconfdir}/mdm/PostLogin
%attr(755,root,root) %config %{_sysconfdir}/mdm/PostLogin/Default.sample
%dir %{_sysconfdir}/mdm/PostSession
%attr(755,root,root) %config %{_sysconfdir}/mdm/PostSession/Default
%dir %{_sysconfdir}/mdm/PreSession
%attr(755,root,root) %config %{_sysconfdir}/mdm/PreSession/Default
%dir %{_sysconfdir}/mdm/SuperInit
%attr(755,root,root) %config %{_sysconfdir}/mdm/SuperInit/Default
%dir %{_sysconfdir}/mdm/SuperPost
%attr(755,root,root) %config %{_sysconfdir}/mdm/SuperPost/Default
%attr(755,root,root) %config %{_sysconfdir}/mdm/XKeepsCrashing
%attr(755,root,root) %config %{_sysconfdir}/mdm/Xsession
%dir %{_sysconfdir}/mdm/modules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mdm/modules/AccessDwellMouseEvents
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mdm/modules/AccessKeyMouseEvents
%config(noreplace) %{_sysconfdir}/mdm/modules/factory-AccessDwellMouseEvents
%config(noreplace) %{_sysconfdir}/mdm/modules/factory-AccessKeyMouseEvents
%attr(640,root,xdm) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mdm/custom.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/mdm/locale.alias
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/mdm
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/mdm-autologin
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.mdm
%dir %{_datadir}/mdm
%{_datadir}/mdm/BuiltInSessions
%{_datadir}/mdm/applications
%dir %{_datadir}/mdm/html-themes
%dir %{_datadir}/mdm/locale
%lang(af) %{_datadir}/mdm/locale/af
%lang(am) %{_datadir}/mdm/locale/am
%lang(ar) %{_datadir}/mdm/locale/ar
%lang(az) %{_datadir}/mdm/locale/az
%lang(be) %{_datadir}/mdm/locale/be
%lang(bg) %{_datadir}/mdm/locale/bg
%lang(bn) %{_datadir}/mdm/locale/bn
%lang(bs) %{_datadir}/mdm/locale/bs
%lang(ca) %{_datadir}/mdm/locale/ca
%lang(cs) %{_datadir}/mdm/locale/cs
%lang(cy) %{_datadir}/mdm/locale/cy
%lang(da) %{_datadir}/mdm/locale/da
%lang(de) %{_datadir}/mdm/locale/de
%lang(el) %{_datadir}/mdm/locale/el
%lang(en_AU) %{_datadir}/mdm/locale/en_AU
%lang(en_CA) %{_datadir}/mdm/locale/en_CA
%lang(en_GB) %{_datadir}/mdm/locale/en_GB
%lang(eo) %{_datadir}/mdm/locale/eo
%lang(es) %{_datadir}/mdm/locale/es
%lang(et) %{_datadir}/mdm/locale/et
%lang(eu) %{_datadir}/mdm/locale/eu
%lang(fa) %{_datadir}/mdm/locale/fa
%lang(fi) %{_datadir}/mdm/locale/fi
%lang(fr) %{_datadir}/mdm/locale/fr
%lang(fr_CA) %{_datadir}/mdm/locale/fr_CA
%lang(frp) %{_datadir}/mdm/locale/frp
%lang(ga) %{_datadir}/mdm/locale/ga
%lang(gd) %{_datadir}/mdm/locale/gd
%lang(gl) %{_datadir}/mdm/locale/gl
%lang(he) %{_datadir}/mdm/locale/he
%lang(hi) %{_datadir}/mdm/locale/hi
%lang(hr) %{_datadir}/mdm/locale/hr
%lang(hu) %{_datadir}/mdm/locale/hu
%lang(ia) %{_datadir}/mdm/locale/ia
%lang(id) %{_datadir}/mdm/locale/id
%lang(ii) %{_datadir}/mdm/locale/ii
%lang(is) %{_datadir}/mdm/locale/is
%lang(it) %{_datadir}/mdm/locale/it
%lang(ja) %{_datadir}/mdm/locale/ja
%lang(ka) %{_datadir}/mdm/locale/ka
%lang(kab) %{_datadir}/mdm/locale/kab
%lang(kk) %{_datadir}/mdm/locale/kk
%lang(km) %{_datadir}/mdm/locale/km
%lang(ko) %{_datadir}/mdm/locale/ko
%lang(ksw) %{_datadir}/mdm/locale/ksw
%lang(ku) %{_datadir}/mdm/locale/ku
%lang(ky) %{_datadir}/mdm/locale/ky
%lang(lo) %{_datadir}/mdm/locale/lo
%lang(lt) %{_datadir}/mdm/locale/lt
%lang(lv) %{_datadir}/mdm/locale/lv
%lang(mg) %{_datadir}/mdm/locale/mg
%lang(ml) %{_datadir}/mdm/locale/ml
%lang(mr) %{_datadir}/mdm/locale/mr
%lang(ms) %{_datadir}/mdm/locale/ms
%lang(mus) %{_datadir}/mdm/locale/mus
%lang(my) %{_datadir}/mdm/locale/my
%lang(nb) %{_datadir}/mdm/locale/nb
%lang(nds) %{_datadir}/mdm/locale/nds
%lang(ne) %{_datadir}/mdm/locale/ne
%lang(nl) %{_datadir}/mdm/locale/nl
%lang(nn) %{_datadir}/mdm/locale/nn
%lang(oc) %{_datadir}/mdm/locale/oc
%lang(om) %{_datadir}/mdm/locale/om
%lang(pa) %{_datadir}/mdm/locale/pa
%lang(pap) %{_datadir}/mdm/locale/pap
%lang(pl) %{_datadir}/mdm/locale/pl
%lang(pt) %{_datadir}/mdm/locale/pt
%lang(pt_BR) %{_datadir}/mdm/locale/pt_BR
%lang(ro) %{_datadir}/mdm/locale/ro
%lang(ru) %{_datadir}/mdm/locale/ru
%lang(rw) %{_datadir}/mdm/locale/rw
%lang(sc) %{_datadir}/mdm/locale/sc
%lang(shn) %{_datadir}/mdm/locale/shn
%lang(si) %{_datadir}/mdm/locale/si
%lang(sk) %{_datadir}/mdm/locale/sk
%lang(sl) %{_datadir}/mdm/locale/sl
%lang(sq) %{_datadir}/mdm/locale/sq
%lang(sr) %{_datadir}/mdm/locale/sr
%lang(sr@latin) %{_datadir}/mdm/locale/sr@latin
%lang(sv) %{_datadir}/mdm/locale/sv
%lang(ta) %{_datadir}/mdm/locale/ta
%lang(tg) %{_datadir}/mdm/locale/tg
%lang(th) %{_datadir}/mdm/locale/th
%lang(tr) %{_datadir}/mdm/locale/tr
%lang(uk) %{_datadir}/mdm/locale/uk
%lang(ur) %{_datadir}/mdm/locale/ur
%lang(uz) %{_datadir}/mdm/locale/uz
%lang(vi) %{_datadir}/mdm/locale/vi
%lang(zh_CN) %{_datadir}/mdm/locale/zh_CN
%lang(zh_HK) %{_datadir}/mdm/locale/zh_HK
%lang(zh_TW) %{_datadir}/mdm/locale/zh_TW
%{_datadir}/mdm/pixmaps
%{_datadir}/mdm/recovery
%{_datadir}/mdm/themes
%{_datadir}/mdm/defaults.conf
%{_datadir}/mdm/factory-defaults.conf
%{_datadir}/mdm/gtk-preview.png
%{_datadir}/mdm/mdmsetup.glade
%{_datadir}/xsessions/ssh.desktop
%{_iconsdir}/hicolor/*x*/apps/mdm.png
%{_iconsdir}/hicolor/*x*/apps/mdmflexiserver.png
%{_iconsdir}/hicolor/*x*/apps/mdmsetup.png
%{_iconsdir}/hicolor/scalable/apps/mdmflexiserver.svg
%{_iconsdir}/hicolor/scalable/apps/mdmsetup.svg
%{_mandir}/man1/mdm.1*
%attr(1770,root,xdm) %dir /var/lib/mdm
%attr(750,xdm,xdm) %dir /var/log/mdm
