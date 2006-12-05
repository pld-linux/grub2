# TODO:
#  - rewrite summary/desc ? GRUB2 has nothing to see with GRUB
#
# Conditional build:
%bcond_with	static	# build static binaries
#
Summary:	GRand Unified Bootloader
Summary(de):	GRUB2 - ein Bootloader für x86 und ppc
Summary(pl):	GRUB2 - bootloader dla x86 i ppc
Summary(pt_BR):	Gerenciador de inicialização GRUB2
Name:		grub2
Version:	1.95
Release:	0.1
License:	GPL v2
Group:		Base
Source0:	ftp://alpha.gnu.org/gnu/grub/grub-%{version}.tar.gz
# Source0-md5:	4ea234d8fc5d551f61bc65e553e51399
URL:		http://www.gnu.org/software/grub/grub-2.en.html
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	libtool
%ifarch %{ix86} %{x8664}
BuildRequires:	lzo-devel >= 1.0.2
%endif
BuildRequires:	ncurses-devel
#BuildRequires:	ruby >= 1.6
BuildRequires:	sed >= 4.0
%if %{with static}
BuildRequires:	glibc-static
%ifarch %{ix86} %{x8664}
BuildRequires:	lzo-static
%endif
BuildRequires:	ncurses-static
%endif
BuildRequires:	rpmbuild(macros) >= 1.213
Provides:	bootloader
ExclusiveArch:	%{ix86} %{x8664} ppc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_bindir		%{_sbindir}
%define		_libdir		/boot
%define		_datadir	%{_libdir}/%{name}

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

%prep
%setup -q -n grub-%{version}
sed -i -e 's#AC_INIT(GRUB,#AC_INIT(GRUB2,#g' configure.ac
sed -i -e 's,/boot/grub,%{_datadir},' \
	kern/i386/efi/startup.S \
	kern/i386/pc/startup.S \
	util/grub-emu.c \
	util/i386/pc/grub-install.in \
	util/i386/pc/grub-mkdevicemap.c \
	util/i386/pc/grub-probe.c \
	util/i386/pc/grub-setup.c \
	util/powerpc/ieee1275/grub-install.in

%build
cp -f /usr/share/automake/config.sub .
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
#for rmk in conf/*.rmk; do
#  ruby genmk.rb < $rmk > `echo $rmk | sed 's/\.rmk$/.mk/'`
#done
CFLAGS="-Os %{?debug:-g}"; export CFLAGS
%configure \
	BUILD_CFLAGS="$CFLAGS"

%{__make} \
	BUILD_CFLAGS="$CFLAGS" \
%if %{with static}
%ifarch %{ix86} %{x8664}
	grub_setup_LDFLAGS="-s -static" \
	grub_mkimage_LDFLAGS="-s -static -llzo" \
%else
	grub_mkimage_LDFLAGS="-s -static" \
%endif
	grub_emu_LDFLAGS="-s -static -lncurses -ltinfo" \
%endif
	pkgdatadir="%{_libdir}/%{name}"


%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgdatadir="%{_libdir}/%{name}"

%ifarch ppc
install grubof $RPM_BUILD_ROOT%{_libdir}/%{name}
%endif
%ifarch %{ix86} %{x8664}
mv -f $RPM_BUILD_ROOT%{_sbindir}/{grub-install,%{name}-install}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_libdir}/%{name}
%attr(754,root,root) %{_sbindir}/grub-emu
%attr(754,root,root) %{_sbindir}/grub-mkimage
%attr(754,root,root) %{_sbindir}/grub2-install
%ifarch %{ix86} %{x8664}
%attr(754,root,root) %{_sbindir}/grub-mkdevicemap
%attr(754,root,root) %{_sbindir}/grub-probe
%attr(754,root,root) %{_sbindir}/grub-setup
%endif
