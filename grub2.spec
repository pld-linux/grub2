# TODO:
#  - rewrite summary/desc ? GRUB2 has nothing to see with GRUB
#
# Conditional build:
%bcond_with	static	# build static binaries
#
%define		_snap	20050330
Summary:	GRand Unified Bootloader
Summary(pl):	GRUB2 - bootloader dla x86 i ppc
Summary(pt_BR):	Gerenciador de inicialização GRUB2
Summary(de):	GRUB2 - ein Bootloader für x86 und ppc
Name:		grub2
Version:	1.90
Release:	0.%{_snap}.0.1
License:	GPL v2
Group:		Base
Source0:	%{name}-%{_snap}.tar.gz
# Source0-md5:	cbeaefb16b4cebfd67cb8198fef3e190
URL:		http://www.gnu.org/software/grub/grub-2.en.html
BuildRequires:	autoconf >= 2.53
BuildRequires:	libtool
%ifarch %{ix86} amd64
BuildRequires:	lzo-devel >= 1.0.2
%endif
BuildRequires:	ncurses-devel
#BuildRequires:	ruby >= 1.6
BuildRequires:	sed >= 4.0
%if %{with static}
BuildRequires:	glibc-static
%ifarch %{ix86} amd64
BuildRequires:	lzo-static
%endif
BuildRequires:	ncurses-static
%endif
Provides:	bootloader
ExclusiveArch:	%{ix86} amd64 ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_bindir		%{_sbindir}
%define		_libdir		/boot
%ifarch amd64
%define		amd64	1
%endif

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
%setup -q -n %{name}
sed 's_grubof_%{_libdir}/%{name}/grubof_' \
	-i util/powerpc/ieee1275/grub-mkimage.c
sed '/i\[\[3456\]\]86)/a  x86_64) host_cpu=i386 ;;' \
	-i configure.ac
sed 's_"/boot/grub"_"%{_libdir}/%{name}"_' \
	-i util/grub-emu.c \
	-i util/i386/pc/grub-setup.c \
	-i kern/i386/pc/startup.S

%build
cp -f /usr/share/automake/config.sub .
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
#for rmk in conf/*.rmk; do
#  ruby genmk.rb < $rmk > `echo $rmk | sed 's/\.rmk$/.mk/'`
#done
CFLAGS="-Os %{?debug:-g}" ; export CFLAGS
%configure \
	BUILD_CC="%{__cc} %{?amd64:-m32} -I%{_includedir}/ncurses" \
%ifarch amd64
	LD="%{__ld} -melf_i386" \
%endif
	BUILD_CFLAGS="$CFLAGS"

%{__make} \
	BUILD_CFLAGS="$CFLAGS" \
%if %{with static}
%ifarch %{ix86} amd64
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_libdir}/%{name}
%attr(754,root,root) %{_sbindir}/grub-emu
%attr(754,root,root) %{_sbindir}/grub-mkimage
%ifarch %{ix86} amd64
%attr(754,root,root) %{_sbindir}/grub-setup
%endif
