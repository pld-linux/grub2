#
# TODO:
# - check VGA patch - doesn't work good, 0.92 works fine
#
# Conditional build:
%bcond_with	splashimage	# removes some ethernet cards support
				# (too much memory occupied?)
#

%define		_snap	270305
Summary:	GRand Unified Bootloader
Summary(pl):	GRUB2 - bootloader dla x86
Summary(pt_BR):	Gerenciador de inicialização GRUB2
Summary(de):	GRUB2 - ein Bootloader für x86
Name:		grub2
Version:	2.0
Release:	0.%{_snap}.1
License:	GPL
Group:		Base
Source0:	%{name}-%{_snap}.tar.gz
# Source0-md5:	4f5b46206d2724a54b1be0744fd03061
Source1:	grub-linux-menu.lst
Source2:	grub-rebootin.awk
Source3:	grub_functions.sh
Source4:	grub-splash.xpm.gz
# Source4-md5:	2842e2955603e3b6d722690b3cdd48a9
URL:		http://www.gnu.org/software/grub/grub-2.en.html
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	lzo-devel >= 1.0.2
BuildRequires:	ncurses-devel
# needed for 'cmp' program
Requires:	diffutils
Provides:	bootloader
ExclusiveArch:	%{ix86} amd64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_libdir		/boot

%description
GRUB is a GPLed bootloader intended to unify bootloading across x86
operating systems. In addition to loading the Linux and *BSD kernels,
it implements the Multiboot standard, which allows for flexible
loading of multiple boot images (needed for modular kernels such as
the GNU Hurd).

%description -l de
GRUB (GRand Unified Boot-loader) ist ein Bootloader, der oft auf
Rechnern eingesetzt wird, auf denen das freie Betriebssystem Linux
läuft. GRUB löst den betagten LILO (Linux-Loader) ab.

GRUB wurde innerhalb des GNU Hurd-Projektes als Boot-Loader entwickelt
und wird unter der GPL vertrieben. Aufgrund seiner höheren
Flexibilität verdrängt GRUB in vielen Linux-Distributionen den
traditionellen Boot-Loader LILO.

%description -l es
Éste es GRUB - Grand Unified Boot Loader - un administrador de
inicialización capaz de entrar en la mayoría de los sistemas
operacionales libres - Linux, FreeBSD, NetBSD, GNU Mach, etc. como
también en la mayoría de los sistemas operacionales comerciales para
PC.

El administrador GRUB puede ser una buena alternativa a LILO, para
usuarios conmás experiencia y que deseen obtener más recursos de su
cargador de inicialización (boot loader).

%description -l pl
GRUB jest bootloaderem na licencji GNU, maj±cym na celu unifikacjê
procesu bootowania na systemach x86. Potrafi nie tylko ³adowaæ j±dra
Linuksa i *BSD: posiada równie¿ implementacje standardu Multiboot,
który pozwala na elastyczne ³adowanie wielu obrazów bootowalnych
(czego wymagaj± modu³owe j±dra, takie jak GNU Hurd).

%description -l pt_BR
Esse é o GRUB - Grand Unified Boot Loader - um gerenciador de boot
capaz de entrar na maioria dos sistemas operacionais livres - Linux,
FreeBSD, NetBSD, GNU Mach, etc. assim como na maioria dos sistemas
operacionais comerciais para PC.

O GRUB pode ser uma boa alternativa ao LILO, para usuários mais
avançados e que querem mais recursos de seu boot loader.

%package nb
Summary:	Grub's network boot image for the Network Image Proposal
Summary(pl):	Obraz dla gruba s³u¿±cy technologii Network Image Proposal
Group:		Networking/Admin

%description nb
This is a network boot image for the Network Image Proposal used by
some network boot loaders, such as Etherboot. This is mostly the same
as Stage 2, but it also sets up a network and loads a configuration
file from the network.

%description nb -l pl
To jest obraz s³u¿±cy zdalnemu uruchamianiu komputera bezdyskowego,
oparty na standardzie nazwanym 'Network Image Proposal'. Jest niemal
identyczny z tym ze Stage 2, ale uruchamia sieæ oraz ³aduje z niej
plik konfiguracyjny.

%package pxe
Summary:	Grub's network boot image for the Preboot Execution Environment
Summary(pl):	Obraz dla gruba s³u¿±cy technologii Preboot Execution Environment
Group:		Networking/Admin

%description pxe
This is another network boot image for the Preboot Execution
Environment used by several Netboot ROMs. This is identical to nbgrub,
except for the format. This is mostly the same as Stage 2, but it also
sets up a network and loads a configuration file from the network.

%description pxe -l pl
To jest obraz s³u¿±cy zdalnemu uruchamianiu komputera bezdyskowego,
oparty na standardzie nazwanym 'Preboot Execution Environment' (PXE).
Jest niemal identyczny z tym ze Stage 2, ale uruchamia sieæ oraz
³aduje z niej plik konfiguracyjny.

%prep
%setup -q -n %{name}

rm -rf doc/*info*

%build
cp -f /usr/share/automake/config.sub .
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
CFLAGS="-Os %{?debug:-g}" ; export CFLAGS
%configure \
%if %{without splashimage}
	--enable-3c503 \
	--enable-3c507 \
	--enable-3c509 \
	--enable-3c529 \
	--enable-3c595 \
	--enable-3c90x \
	--enable-compex-rl2000-fix \
	--enable-cs89x0 \
	--enable-davicom \
	--enable-depca \
	--enable-diskless \
	--enable-e1000 \
	--enable-eepro \
	--enable-eepro100 \
	--enable-epic100 \
	--enable-exos205 \
	--enable-lance \
	--enable-natsemi \
	--enable-ne \
	--enable-ne2100 \
	--enable-ni5010 \
	--enable-ni5210 \
	--enable-ni6510 \
	--enable-rtl8139 \
	--enable-sk-g16 \
	--enable-smc9000 \
	--enable-tg3 \
	--enable-tiara \
	--enable-tulip \
	--enable-via-rhine \
	--enable-w89c840 \
	--enable-wd \
%endif
	--disable-auto-linux-mem-opt
# if you want to enable following cards for pxeboot comment out patches 8 & 9
# and comment out --enable-e1000 & --enable-tg3 cards:
#       --enable-ns8390 \
#       --enable-sis900
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-boot

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_libdir}/grub/%{_arch}-*/* \
	$RPM_BUILD_ROOT%{_libdir}/grub/

install %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/grub/menu.lst
install %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}/rebootin
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/rc-boot
install %{SOURCE4} $RPM_BUILD_ROOT%{_libdir}/grub/splash.xpm.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc TODO BUGS NEWS ChangeLog docs/menu.lst
%dir %{_libdir}/grub
%{_libdir}/grub/*stage*
%{_libdir}/grub/splash.xpm.gz
%config(noreplace) %verify(not md5 mtime size) %{_libdir}/grub/menu.lst
%attr(754,root,root) %{_bindir}/*
%attr(754,root,root) %{_sbindir}/*
%{_infodir}/*.info*
%{_mandir}/*/*
/etc/sysconfig/rc-boot/%{name}_functions.sh

%if %{without splashimage}
%files nb
%defattr(644,root,root,755)
%{_libdir}/grub/nbgrub

%files pxe
%defattr(644,root,root,755)
%{_libdir}/grub/pxegrub
%endif
