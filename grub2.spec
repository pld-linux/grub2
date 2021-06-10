# TODO
# - reap out which in probe scripts and drop R: which
# - subpackages? e.g. modules and utils
# - check where is that locale path: /boot/grub/locale and fix it or change it
# - grubemu notes
#   --enable-grub-emu-usb conflicts with --enable-grub-emu-pci, emu-pci seems experimental
#   - to build and install the `grub-emu' debugging utility we need to re-run build with --target=emu
#   - put grub-emu to subpackage if it is fixed
#
# Conditional build:
%bcond_with	grubemu		# grub-emu debugging utility
%bcond_without	efiemu		# efiemu runtimes
%bcond_without	unifont		# unifont based fonts
%bcond_without	arc		# MIPS ARC platform support
%bcond_without	coreboot	# coreboot/linuxbios platform support (x86/arm specific)
%bcond_without	efi		# EFI platform support
%bcond_without	ieee1275	# ieee1275 platform support (x86/ppc/sparc specific)
%bcond_without	loongson	# MIPS loongson platform support (mipsel specific)
%bcond_without	multiboot	# multiboot platform support (x86/arm specific)
%bcond_without	pc		# PC BIOS platform support (x86 specific)
%bcond_without	qemu		# qemu platform support (x86/mips specific)
%bcond_without	uboot		# ARM uBoot platform support
%bcond_without	xen		# Xen platform support (x86 specific)
%bcond_without	xen_pvh		# Xen PVH platform support (x86 specific)

%ifnarch mips mipsel mips64 mips64el
%undefine	with_arc
%endif
%ifnarch %{ix86} %{x8664} x32 %{arm}
%undefine	with_coreboot
%endif
%ifnarch %{ix86} %{x8664} x32 %{arm} aarch64 ia64
%undefine	with_efi
%endif
%ifnarch %{ix86} %{x8664} x32 ppc ppc64 sparc64
%undefine	with_ieee1275
%endif
%ifnarch mipsel mips64el
%undefine	with_loongson
%endif
%ifnarch %{ix86} %{x8664} x32
%undefine	with_multiboot
%undefine	with_pc
%undefine	with_xen
%undefine	with_xen_pvh
%endif
%ifnarch %{ix86} mips mipsel mips64 mips64el
%undefine	with_qemu
%endif
%ifnarch %{arm}
%undefine	with_uboot
%endif

# these require unifont
%if %{without unifont}
%undefine	with_coreboot
%undefine	with_loongson
%undefine	with_qemu
%endif

%ifnarch %{x8664} x32
# non-x86_64 arch doesn't support this
%undefine	with_efiemu
%endif

# the 'most natural' platform should go last
%ifarch %{ix86} %{x8664} x32
%define		platforms %{?with_coreboot:coreboot} %{?with_ieee1275:ieee1275} %{?with_multiboot:multiboot} %{?with_qemu:qemu} %{?with_xen:xen xen_pvh} %{?with_efi:efi} %{?with_pc:pc}
%endif
%ifarch %{arm}
%define		platforms %{?with_efi:efi} %{?with_uboot:uboot}
%endif
%ifarch aarch64 ia64 riscv32 riscv64
%define		platforms efi
%endif
%ifarch mips mips64
%define		platforms arc
%endif
%ifarch mipsel mips64el
%define		platforms %{?with_arc:arc} %{?with_loongson:loongson}
%endif
%ifarch ppc ppc64 sparc64
%define		platforms ieee1275
%endif

%ifarch %{ix86}
%define	coreboot_arch	i386
%define	efi_arch	i386
%define	ieee1275_arch	i386
%define	qemu_arch	i386
%define	qemu_plat	qemu
%define	xen_arch	i386
%endif
%ifarch %{x8664} x32
%define	coreboot_arch	i386
%define	efi_arch	x86_64
%define	ieee1275_arch	i386
%define	qemu_arch	i386
%define	qemu_plat	qemu
%define	xen_arch	x86_64
%endif
%ifarch %{arm}
%define	coreboot_arch	arm
%define	efi_arch	arm
%endif
%ifarch aarch64
%define	efi_arch	arm64
%endif
%ifarch ia64
%define	efi_arch	ia64
%endif
%ifarch mips mips64
%define	arc_arch	mips
%define	qemu_arch	mips
%define	qemu_plat	qemu_mips
%endif
%ifarch mipsel mips64el
%define	arc_arch	mipsel
%define	qemu_arch	mipsel
%define	qemu_plat	qemu_mips
%endif
%ifarch ppc ppc64
%define	ieee1275_arch	powerpc
%endif
%ifarch riscv32
%define	efi_arch	riscv32
%endif
%ifarch riscv64
%define	efi_arch	riscv64
%endif
%ifarch sparc64
%define	ieee1275_arch	sparc64
%endif

Summary:	GRand Unified Bootloader
Summary(de.UTF-8):	GRUB2 - ein Bootloader für x86 und ppc
Summary(hu.UTF-8):	GRUB2 - rendszerbetöltő x86 és ppc gépekhez
Summary(pl.UTF-8):	GRUB2 - bootloader dla x86 i ppc
Summary(pt_BR.UTF-8):	Gerenciador de inicialização GRUB2
Name:		grub2
Version:	2.06
Release:	1
License:	GPL v2
Group:		Base
Source0:	https://ftp.gnu.org/gnu/grub/grub-%{version}.tar.xz
# Source0-md5:	cf0fd928b1e5479c8108ee52cb114363
Source1:	update-grub
Source2:	update-grub.8
Source3:	grub.sysconfig
Source4:	grub-custom.cfg
Patch1:		pld-sysconfdir.patch
Patch2:		grub-garbage.patch
Patch3:		grub-lvmdevice.patch
Patch4:		pld-mkconfigdir.patch
Patch5:		grub-mkconfig-diagnostics.patch
Patch6:		posix.patch
Patch7:		%{name}-fonts_path.patch
Patch9:		just-say-linux.patch
Patch10:	ignore-kernel-symlinks.patch
Patch11:	choose-preferred-initrd.patch
Patch12:	%{name}-cfg.patch
Patch13:	efi-net-fix.patch
Patch14:	blscfg.patch
URL:		http://www.gnu.org/software/grub/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11.1-1
BuildRequires:	bison >= 2.3
BuildRequires:	device-mapper-devel >= 1.02.34
BuildRequires:	flex >= 2.5.35
BuildRequires:	fonts-TTF-DejaVu
%if %{with unifont}
BuildRequires:	fonts-misc-unifont
%endif
BuildRequires:	freetype-devel >= 2.1.5
BuildRequires:	gawk
BuildRequires:	gcc >= 6:5.1
BuildRequires:	gettext-tools >= 0.18.3
BuildRequires:	glibc-localedb-all
BuildRequires:	glibc-static
BuildRequires:	help2man
BuildRequires:	libfuse-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRequires:	python >= 1:2.6
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
BuildRequires:	xz
BuildRequires:	xz-devel
%ifarch %{x8664}
BuildRequires:	/usr/lib/libc.so
%if "%{pld_release}" == "ac"
BuildRequires:	libgcc32
%else
BuildRequires:	gcc-multilib-32
%endif
%endif
Requires:	%{name}-platform = %{version}-%{release}
Requires:	pld-release
Requires:	which
%ifarch %{ix86} %{x8664} x32
Suggests:	%{name}-platform-pc
%endif
Suggests:	cdrkit-mkisofs
Suggests:	os-prober
Provides:	bootloader
Conflicts:	grub
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm} aarch64 ia64 mips mipsel mips64 mips64el ppc ppc64 riscv32 riscv64 sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_bindir		%{_sbindir}
%define		_libdir		/lib
%define		_datadir	%{_libdir}
%define		_libexecdir	%{_libdir}/grub
%define		_grubdir	/boot/grub
%define		_localedir	/usr/share/locale

# part of grub code is not relocable (these are not Linux libs)
# stack protector also breaks non-Linux binaries
# any kind of forced optimizations makes grub2 unreliable (random
# reboots and hangs on boot menu screen)
%define		filterout_c	-fPIC -O.
%undefine	_ssp_cflags
%undefine	_fortify_cflags

%description
GRUB is a GPLed bootloader intended to unify bootloading across x86
operating systems. In addition to loading the Linux and *BSD kernels,
it implements the Multiboot standard, which allows for flexible
loading of multiple boot images (needed for modular kernels such as
the GNU Hurd).

GRUB 2 is derived from PUPA which was a research project to
investigate the next generation of GRUB. GRUB 2 has been rewritten
from scratch to clean up everything for modularity and portability.

GRUB 2 targets at the following goals:
- Scripting support, such as conditionals, loops, variables and
  functions.
- Graphical interface.
- Dynamic loading of modules in order to extend itself at the run time
  rather than at the build time.
- Portability for various architectures.
- Internationalization. This includes support for non-ASCII character
  code, message catalogs like gettext, fonts, graphics console, and so
  on.
- Real memory management, to make GNU GRUB more extensible.
- Modular, hierarchical, object-oriented framework for file systems,
  files, devices, drives, terminals, commands, partition tables and OS
  loaders.
- Cross-platform installation which allows for installing GRUB from a
  different architecture.
- Rescue mode saves unbootable cases. Stage 1.5 was eliminated.
- Fix design mistakes in GRUB Legacy, which could not be solved for
  backward-compatibility, such as the way of numbering partitions.

%description -l de.UTF-8
GRUB (GRand Unified Boot-loader) ist ein Bootloader, der oft auf
Rechnern eingesetzt wird, auf denen das freie Betriebssystem Linux
läuft. GRUB löst den betagten LILO (Linux-Loader) ab.

GRUB wurde innerhalb des GNU Hurd-Projektes als Boot-Loader entwickelt
und wird unter der GPL vertrieben. Aufgrund seiner höheren
Flexibilität verdrängt GRUB in vielen Linux-Distributionen den
traditionellen Boot-Loader LILO.

%description -l hu.UTF-8
GRUB egy GPL liszenszű rendszerbetöltő. Linux és *BSD kernelek
betöltése mellett támogatja a Multiboot standard-ot, amely lehetővé
teszi boot képek betöltését (moduláris kerneleknek kell, mint pl. a
GNU Hurd).

GRUB2 céljai a következők:
- szkriptelés támogatása, úgymint feltételek, ciklusok, változók,
  függvények.
- grafikus felület
- modulok dinamikus betöltése futási időben
- hordozhatóság több architektúrára
- többnyelvűség: nem-ASCII karakterek támogatása, üzenetkatalógusok,
  mint gettext, betűtípusok, grafikus konzolon, és így tovább
- valós memória kezelés, amellyel még bővíthetőbbé tehetjük
- moduláris, hierarchikus, objektum-orientált keretrendszer
  fájlrendszerekhez, fájlokhoz, eszközökhöz, meghajtókhoz,
  terminálokhoz, parancsokhoz, partíciós táblákhoz és OS betöltőkhöz

%description -l es.UTF-8
Éste es GRUB - Grand Unified Boot Loader - un administrador de
inicialización capaz de entrar en la mayoría de los sistemas
operacionales libres - Linux, FreeBSD, NetBSD, GNU Mach, etc. como
también en la mayoría de los sistemas operacionales comerciales para
PC.

El administrador GRUB puede ser una buena alternativa a LILO, para
usuarios conmás experiencia y que deseen obtener más recursos de su
cargador de inicialización (boot loader).

%description -l pl.UTF-8
GRUB jest bootloaderem na licencji GNU GPL, mającym na celu unifikację
procesu bootowania na systemach x86. Potrafi nie tylko ładować jądra
Linuksa i *BSD: posiada również implementację standardu Multiboot,
który pozwala na elastyczne ładowanie wielu obrazów bootowalnych
(czego wymagają modułowe jądra, takie jak GNU Hurd).

%description -l pt_BR.UTF-8
Esse é o GRUB - Grand Unified Boot Loader - um gerenciador de boot
capaz de entrar na maioria dos sistemas operacionais livres - Linux,
FreeBSD, NetBSD, GNU Mach, etc. assim como na maioria dos sistemas
operacionais comerciais para PC.

O GRUB pode ser uma boa alternativa ao LILO, para usuários mais
avançados e que querem mais recursos de seu boot loader.

%package -n bash-completion-%{name}
Summary:	bash-completion for GRUB
Summary(pl.UTF-8):	Bashowe uzupełnianie nazw dla GRUB-a
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion
BuildArch:	noarch

%description -n bash-completion-%{name}
This package provides bash-completion for GRUB.

%description -n bash-completion-%{name} -l pl.UTF-8
Pakiet ten dostarcza bashowe uzupełnianie nazw dla GRUB-a.

%package fonts
Summary:	Fonts for GRUB
Summary(pl.UTF-8):	Fonty dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}

%description fonts
Fonts for GRUB.

%description fonts -l pl.UTF-8
Fonty dla GRUB-a.

%package platform-arc
Summary:	MIPS ARC platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy MIPS ARC dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-platform = %{version}-%{release}

%description platform-arc
MIPS ARC platform support for GRUB.

%description platform-arc -l pl.UTF-8
Obsługa platformy MIPS ARC dla GRUB-a.

%package platform-coreboot
Summary:	Coreboot (LinuxBIOS) platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy Coreboot (LinuxBIOS) dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-fonts = %{version}-%{release}
Provides:	%{name}-platform = %{version}-%{release}

%description platform-coreboot
Coreboot (LinuxBIOS) platform support for GRUB.

%description platform-coreboot -l pl.UTF-8
Obsługa platformy Coreboot (LinuxBIOS) dla GRUB-a.

%package platform-efi
Summary:	(U)EFI platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy (U)EFI dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}
Suggests:	efibootmgr
Provides:	%{name}-platform = %{version}-%{release}

%description platform-efi
(U)EFI platform support for GRUB.

%description platform-efi -l pl.UTF-8
Obsługa platformy (U)EFI dla GRUB-a.

%package platform-ieee1275
Summary:	IEEE 1275 (OpenFirmware) platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy IEEE 1275 (OpenFirmware) dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-platform = %{version}-%{release}

%description platform-ieee1275
IEEE 1275 (OpenFirmware) platform support for GRUB.

%description platform-ieee1275 -l pl.UTF-8
Obsługa platformy IEEE 1275 (OpenFirmware) dla GRUB-a.

%package platform-loongson
Summary:	MIPS Loongson platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy MIPS Loongson dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-fonts = %{version}-%{release}
Provides:	%{name}-platform = %{version}-%{release}

%description platform-loongson
MIPS Loongson (yeelong, fuloong) platform support for GRUB.

%description platform-loongson -l pl.UTF-8
Obsługa platformy MIPS Loongson (yeelong, fuloong) dla GRUB-a.

%package platform-multiboot
Summary:	Multiboot platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy Multiboot dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-platform = %{version}-%{release}

%description platform-multiboot
Multiboot platform support for GRUB.

%description platform-multiboot -l pl.UTF-8
Obsługa platformy Multiboot dla GRUB-a.

%package platform-pc
Summary:	PC BIOS platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy PC BIOS dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-platform = %{version}-%{release}

%description platform-pc
PC BIOS platform support for GRUB.

%description platform-pc -l pl.UTF-8
Obsługa platformy PC BIOS dla GRUB-a.

%package platform-qemu
Summary:	Qemu platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy Qemu dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-fonts = %{version}-%{release}
Provides:	%{name}-platform = %{version}-%{release}

%description platform-qemu
Qemu platform support for GRUB.

%description platform-qemu -l pl.UTF-8
Obsługa platformy Qemu dla GRUB-a.

%package platform-uboot
Summary:	ARM uBoot platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy ARM uBoot dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-platform = %{version}-%{release}

%description platform-uboot
ARM uBoot platform support for GRUB.

%description platform-uboot -l pl.UTF-8
Obsługa platformy ARM uBoot dla GRUB-a.

%package platform-xen
Summary:	Xen platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy Xen dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-platform = %{version}-%{release}

%description platform-xen
Xen platform support for GRUB.

%description platform-xen -l pl.UTF-8
Obsługa platformy Xen dla GRUB-a.

%package platform-xen_pvh
Summary:	Xen PVH platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy Xen PVH dla GRUB-a
Group:		Base
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-platform = %{version}-%{release}

%description platform-xen_pvh
Xen PVH platform support for GRUB.

%description platform-xen_pvh -l pl.UTF-8
Obsługa platformy Xen PVH dla GRUB-a.

%package mkfont
Summary:	GRUB font files converter
Summary(pl.UTF-8):	Konwerter plików fontów GRUB-a
Group:		Base

%description mkfont
Converts common font file formats into PF2.

%description mkfont -l pl.UTF-8
Program do konwersji popularnych formatów plików fontów do PF2.

%package theme-starfield
Summary:	starfield theme for GRUB
Summary(pl.UTF-8):	Motyw starfield dla GRUB-a
Requires:	%{name} = %{version}-%{release}
Group:		Base

%description theme-starfield
starfield theme for GRUB.

%description theme-starfield -l pl.UTF-8
Motyw starfield dla GRUB-a.

%prep
%setup -q -n grub-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p0
%patch13 -p1
%patch14 -p1

# we don't have C.utf-8 and need an UTF-8 locale for build
sed -i -e 's/LC_ALL=C.UTF-8/LC_ALL=en_US.utf-8/g' po/Makefile* po/Rules*

%build
# if gold is used then grub doesn't even boot
# https://savannah.gnu.org/bugs/?34539
# http://sourceware.org/bugzilla/show_bug.cgi?id=14196
install -d our-ld
ln -f -s /usr/bin/ld.bfd our-ld/ld
export PATH=$(pwd)/our-ld:$PATH

## not only the typical autotools stuff
#./autogen.sh

#{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

for platform in %{platforms} ; do
	install -d build-${platform}
	cd build-${platform}

	if [ "$platform" != "efi" ] ; then
		platform_opts="--enable-efiemu%{!?with_efiemu:=no}"
	else
		platform_opts=""
	fi

	ln -f -s ../configure .
	# mawk stalls at ./genmoddep.awk, so force gawk
	AWK=gawk \
	%configure \
		--with-platform=${platform} \
		--disable-werror \
		--enable-grub-themes \
	%if %{with grubemu}
		--enable-grub-emu-usb \
		--enable-grub-emu-sdl \
		--enable-grub-emu-pci \
	%endif
		$platform_opts \
		TARGET_LDFLAGS=-static

	%{__make} -j1 -C po update-gmo
	%{__make}
	cd ..
done

%install
rm -rf $RPM_BUILD_ROOT

for platform in %{platforms} ; do
	cd build-${platform}
	%{__make} install \
		pkgdatadir=%{_libexecdir} \
		pkglibdir=%{_libexecdir} \
		DESTDIR=$RPM_BUILD_ROOT
	cd ..
done

# not in Th (?)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/de@hebrew
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/en@{arabic,cyrillic,greek,hebrew,piglatin}

%find_lang grub

# this must be after 'make install'
install -d $RPM_BUILD_ROOT%{_libexecdir}/locale

install -d $RPM_BUILD_ROOT%{_grubdir}
cp -p docs/grub.cfg $RPM_BUILD_ROOT%{_grubdir}

# grub.d/41_custom
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_grubdir}/custom.cfg
%{__rm} $RPM_BUILD_ROOT/lib/grub.d/40_custom

install -p %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/update-grub
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man8/update-grub.8

install -d $RPM_BUILD_ROOT/etc/sysconfig
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/grub

# rm -f, because it sometimes exists, sometimes not, depending which texlive you have installed
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# platform specific, unnecessarily always installed
%ifnarch %{ix86} %{x8664} x32
%{__rm} $RPM_BUILD_ROOT{%{_sbindir}/grub-bios-setup,%{_mandir}/man8/grub-bios-setup.8}
%endif
%ifnarch sparc64
%{__rm} $RPM_BUILD_ROOT{%{_sbindir}/grub-sparc64-setup,%{_mandir}/man8/grub-sparc64-setup.8}
%endif

# core.img - bootable image generated by grub-mkimage(1) via grub-install(1)
touch $RPM_BUILD_ROOT%{_grubdir}/core.img
touch $RPM_BUILD_ROOT%{_grubdir}/device.map

# needs to be exactly 1KiB
# but we're ghosting it. so whom are we kidding here? :P (maybe %config it in future?)
dd bs=1024 if=/dev/zero count=1 of=$RPM_BUILD_ROOT%{_grubdir}/grubenv

%clean
rm -rf $RPM_BUILD_ROOT

%post -p %{_sbindir}/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun -p %{_sbindir}/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%triggerpostun -- %{name} < 2.00-2
# Note this trigger on version upgrade needed only for upgrade from
# old grub2 packages which contained modules in /boot/grub
# or were built with optimizations enabled
# don't do anything on --downgrade
if [ $1 -le 1 ]; then
	exit 0
fi
echo "Grub was upgraded, trying to setup it to boot sector"
/sbin/grub-install '(hd0)' || :

%triggerpostun -- %{name} < 1.99-7.3
# migrate /etc/grub.d/custom.cfg.rpmsave  -> /boot/grub/custom.cfg
if [ -f %{_sysconfdir}/grub.d/custom.cfg.rpmsave ]; then
	cp -f %{_grubdir}/custom.cfg{,.rpmnew}
	mv -f  %{_sysconfdir}/grub.d/custom.cfg.rpmsave %{_grubdir}/custom.cfg
fi

%files -f grub.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/grub
%attr(755,root,root) %{_sbindir}/grub-editenv
%attr(755,root,root) %{_sbindir}/grub-fstest
%attr(755,root,root) %{_sbindir}/grub-file
%attr(755,root,root) %{_sbindir}/grub-glue-efi
%attr(755,root,root) %{_sbindir}/grub-kbdcomp
%attr(755,root,root) %{_sbindir}/grub-install
%attr(755,root,root) %{_sbindir}/grub-macbless
%attr(755,root,root) %{_sbindir}/grub-menulst2cfg
%attr(755,root,root) %{_sbindir}/grub-mkconfig
%attr(755,root,root) %{_sbindir}/grub-mklayout
%attr(755,root,root) %{_sbindir}/grub-mknetdir
%attr(755,root,root) %{_sbindir}/grub-mkpasswd-pbkdf2
%attr(755,root,root) %{_sbindir}/grub-mkrelpath
%attr(755,root,root) %{_sbindir}/grub-mkrescue
%attr(755,root,root) %{_sbindir}/grub-mkstandalone
%attr(755,root,root) %{_sbindir}/grub-mount
%attr(755,root,root) %{_sbindir}/grub-ofpathname
%attr(755,root,root) %{_sbindir}/grub-reboot
%attr(755,root,root) %{_sbindir}/grub-render-label
%attr(755,root,root) %{_sbindir}/grub-script-check
%attr(755,root,root) %{_sbindir}/grub-set-default
%attr(755,root,root) %{_sbindir}/grub-syslinux2cfg
%attr(755,root,root) %{_sbindir}/update-grub
%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_sbindir}/grub-bios-setup
%{_mandir}/man8/grub-bios-setup.8*
%endif
%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_sbindir}/grub-mkimage
%{_mandir}/man1/grub-mkimage.1*
%else
%attr(755,root,root) %{_sbindir}/grub-probe
%{_mandir}/man8/grub-probe.8*
%endif
%ifarch sparc64
%attr(755,root,root) %{_sbindir}/grub-sparc64-setup
%{_mandir}/man8/grub-sparc64-setup.8*
%endif
%{_mandir}/man1/grub-editenv.1*
%{_mandir}/man1/grub-file.1*
%{_mandir}/man1/grub-fstest.1*
%{_mandir}/man1/grub-glue-efi.1*
%{_mandir}/man1/grub-kbdcomp.1*
%{_mandir}/man1/grub-menulst2cfg.1*
%{_mandir}/man1/grub-mklayout.1*
%{_mandir}/man1/grub-mknetdir.1*
%{_mandir}/man1/grub-mkpasswd-pbkdf2.1*
%{_mandir}/man1/grub-mkrelpath.1*
%{_mandir}/man1/grub-mkrescue.1*
%{_mandir}/man1/grub-mkstandalone.1*
%{_mandir}/man1/grub-mount.1*
%{_mandir}/man1/grub-render-label.1*
%{_mandir}/man1/grub-script-check.1*
%{_mandir}/man1/grub-syslinux2cfg.1*
%{_mandir}/man8/grub-install.8*
%{_mandir}/man8/grub-macbless.8*
%{_mandir}/man8/grub-mkconfig.8*
%{_mandir}/man8/grub-ofpathname.8*
%{_mandir}/man8/grub-reboot.8*
%{_mandir}/man8/grub-set-default.8*
%{_mandir}/man8/update-grub.8*
%if %{with grubemu}
%attr(755,root,root) %{_sbindir}/grub-emu
%{_mandir}/man8/grub-emu.8*
%endif
%{_libexecdir}/grub-mkconfig_lib

%dir %{_grubdir}
%dir %{_libexecdir}
# XXX: check this locale dir location and if it is neccesaary to exist on /boot

%dir %{_libexecdir}/locale
%config(noreplace) %verify(not md5 mtime size) %{_grubdir}/grub.cfg
%config(noreplace) %verify(not md5 mtime size) %{_grubdir}/custom.cfg

# generated by grub at runtime
%ghost %{_grubdir}/device.map
%ghost %{_grubdir}/core.img
%ghost %{_grubdir}/grubenv

%dir /lib/grub.d
%doc /lib/grub.d/README
%attr(755,root,root) /lib/grub.d/00_header
%attr(755,root,root) /lib/grub.d/10_linux
%attr(755,root,root) /lib/grub.d/20_linux_xen
%attr(755,root,root) /lib/grub.d/30_os-prober
%attr(755,root,root) /lib/grub.d/41_custom

%ifarch %{ix86} %{x8664} x32
%attr(755,root,root) %{_sbindir}/grub-probe
%{_mandir}/man8/grub-probe.8*
%endif

%{_infodir}/grub*.info*

%dir %{_datadir}/grub/themes

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/grub

%if %{with unifont}
%files fonts
%defattr(644,root,root,755)
%{_libexecdir}/ascii.h
%{_libexecdir}/ascii.pf2
%{_libexecdir}/euro.pf2
%{_libexecdir}/unicode.pf2
%{_libexecdir}/widthspec.h
%endif

%if %{with arc}
%files platform-arc
%defattr(644,root,root,755)
%dir %{_libexecdir}/%{arc_arch}-arc
%{_libexecdir}/%{arc_arch}-arc/modinfo.sh
%{_libexecdir}/%{arc_arch}-arc/*.lst
%{_libexecdir}/%{arc_arch}-arc/*.mod
%{_libexecdir}/%{arc_arch}-arc/*.module
%{_libexecdir}/%{arc_arch}-arc/config.h
%{_libexecdir}/%{arc_arch}-arc/gdb_grub
%{_libexecdir}/%{arc_arch}-arc/gmodule.pl
%{_libexecdir}/%{arc_arch}-arc/kernel.exec
%{_libexecdir}/%{arc_arch}-arc/kernel.img
%endif

%if %{with coreboot}
%files platform-coreboot
%defattr(644,root,root,755)
%dir %{_libexecdir}/%{coreboot_arch}-coreboot
%{_libexecdir}/%{coreboot_arch}-coreboot/modinfo.sh
%{_libexecdir}/%{coreboot_arch}-coreboot/*.lst
%{_libexecdir}/%{coreboot_arch}-coreboot/*.mod
%{_libexecdir}/%{coreboot_arch}-coreboot/*.module
%{_libexecdir}/%{coreboot_arch}-coreboot/config.h
%{_libexecdir}/%{coreboot_arch}-coreboot/gdb_grub
%{_libexecdir}/%{coreboot_arch}-coreboot/gmodule.pl
%{_libexecdir}/%{coreboot_arch}-coreboot/kernel.exec
%{_libexecdir}/%{coreboot_arch}-coreboot/kernel.img
%endif

%if %{with efi}
%files platform-efi
%defattr(644,root,root,755)
%attr(755,root,root) /lib/grub.d/30_uefi-firmware
%dir %{_libexecdir}/%{efi_arch}-efi
%{_libexecdir}/%{efi_arch}-efi/modinfo.sh
%{_libexecdir}/%{efi_arch}-efi/*.lst
%{_libexecdir}/%{efi_arch}-efi/*.mod
%{_libexecdir}/%{efi_arch}-efi/*.module
%{_libexecdir}/%{efi_arch}-efi/config.h
%{_libexecdir}/%{efi_arch}-efi/gdb_grub
%{_libexecdir}/%{efi_arch}-efi/gmodule.pl
%{_libexecdir}/%{efi_arch}-efi/kernel.exec
%{_libexecdir}/%{efi_arch}-efi/kernel.img
%endif

%if %{with ieee1275}
%files platform-ieee1275
%defattr(644,root,root,755)
%dir %{_libexecdir}/%{ieee1275_arch}-ieee1275
%{_libexecdir}/%{ieee1275_arch}-ieee1275/modinfo.sh
%{_libexecdir}/%{ieee1275_arch}-ieee1275/*.lst
%{_libexecdir}/%{ieee1275_arch}-ieee1275/*.mod
%{_libexecdir}/%{ieee1275_arch}-ieee1275/*.module
%{_libexecdir}/%{ieee1275_arch}-ieee1275/config.h
%{_libexecdir}/%{ieee1275_arch}-ieee1275/gdb_grub
%{_libexecdir}/%{ieee1275_arch}-ieee1275/gmodule.pl
%{_libexecdir}/%{ieee1275_arch}-ieee1275/kernel.exec
%{_libexecdir}/%{ieee1275_arch}-ieee1275/kernel.img
%endif

%if %{with multiboot}
%files platform-multiboot
%defattr(644,root,root,755)
%dir %{_libexecdir}/i386-multiboot
%{_libexecdir}/i386-multiboot/modinfo.sh
%{_libexecdir}/i386-multiboot/*.lst
%{_libexecdir}/i386-multiboot/*.mod
%{_libexecdir}/i386-multiboot/*.module
%{_libexecdir}/i386-multiboot/config.h
%{_libexecdir}/i386-multiboot/gdb_grub
%{_libexecdir}/i386-multiboot/gmodule.pl
%{_libexecdir}/i386-multiboot/kernel.exec
%{_libexecdir}/i386-multiboot/kernel.img
%endif

%if %{with pc}
%files platform-pc
%defattr(644,root,root,755)
%dir %{_libexecdir}/i386-pc
%{_libexecdir}/i386-pc/modinfo.sh
%{_libexecdir}/i386-pc/*.lst
%{_libexecdir}/i386-pc/*.mod
%{_libexecdir}/i386-pc/*.module
%{_libexecdir}/i386-pc/config.h
%{_libexecdir}/i386-pc/gdb_grub
%{_libexecdir}/i386-pc/gmodule.pl
%{_libexecdir}/i386-pc/boot.image
%{_libexecdir}/i386-pc/boot.img
%{_libexecdir}/i386-pc/boot_hybrid.image
%{_libexecdir}/i386-pc/boot_hybrid.img
%{_libexecdir}/i386-pc/cdboot.image
%{_libexecdir}/i386-pc/cdboot.img
%{_libexecdir}/i386-pc/diskboot.image
%{_libexecdir}/i386-pc/diskboot.img
%{_libexecdir}/i386-pc/kernel.exec
%{_libexecdir}/i386-pc/kernel.img
%{_libexecdir}/i386-pc/lnxboot.image
%{_libexecdir}/i386-pc/lnxboot.img
%{_libexecdir}/i386-pc/lzma_decompress.image
%{_libexecdir}/i386-pc/lzma_decompress.img
%{_libexecdir}/i386-pc/pxeboot.image
%{_libexecdir}/i386-pc/pxeboot.img
%if %{with efiemu}
%{_libexecdir}/i386-pc/efiemu*.o
%endif
%endif

%if %{with qemu}
%files platform-qemu
%defattr(644,root,root,755)
%dir %{_libexecdir}/%{qemu_arch}-%{qemu_plat}
%{_libexecdir}/%{qemu_arch}-%{qemu_plat}/modinfo.sh
%{_libexecdir}/%{qemu_arch}-%{qemu_plat}/*.lst
%{_libexecdir}/%{qemu_arch}-%{qemu_plat}/*.mod
%{_libexecdir}/%{qemu_arch}-%{qemu_plat}/*.module
%{_libexecdir}/%{qemu_arch}-%{qemu_plat}/config.h
%{_libexecdir}/%{qemu_arch}-%{qemu_plat}/gdb_grub
%{_libexecdir}/%{qemu_arch}-%{qemu_plat}/gmodule.pl
%{_libexecdir}/%{qemu_arch}-%{qemu_plat}/boot.image
%{_libexecdir}/%{qemu_arch}-%{qemu_plat}/boot.img
%{_libexecdir}/%{qemu_arch}-%{qemu_plat}/kernel.exec
%{_libexecdir}/%{qemu_arch}-%{qemu_plat}/kernel.img
%endif

%if %{with uboot}
%files platform-uboot
%defattr(644,root,root,755)
%dir %{_libexecdir}/arm-uboot
%{_libexecdir}/arm-uboot/modinfo.sh
%{_libexecdir}/arm-uboot/*.lst
%{_libexecdir}/arm-uboot/*.mod
%{_libexecdir}/arm-uboot/*.module
%{_libexecdir}/arm-uboot/config.h
%{_libexecdir}/arm-uboot/gdb_grub
%{_libexecdir}/arm-uboot/gmodule.pl
%{_libexecdir}/arm-uboot/kernel.exec
%{_libexecdir}/arm-uboot/kernel.img
%endif

%if %{with xen}
%files platform-xen
%defattr(644,root,root,755)
%dir %{_libexecdir}/%{xen_arch}-xen
%{_libexecdir}/%{xen_arch}-xen/modinfo.sh
%{_libexecdir}/%{xen_arch}-xen/*.lst
%{_libexecdir}/%{xen_arch}-xen/*.mod
%{_libexecdir}/%{xen_arch}-xen/*.module
%{_libexecdir}/%{xen_arch}-xen/config.h
%{_libexecdir}/%{xen_arch}-xen/gdb_grub
%{_libexecdir}/%{xen_arch}-xen/gmodule.pl
%{_libexecdir}/%{xen_arch}-xen/kernel.exec
%{_libexecdir}/%{xen_arch}-xen/kernel.img
%endif

%if %{with xen_pvh}
%files platform-xen_pvh
%defattr(644,root,root,755)
%dir %{_libexecdir}/i386-xen_pvh
%{_libexecdir}/i386-xen_pvh/modinfo.sh
%{_libexecdir}/i386-xen_pvh/*.lst
%{_libexecdir}/i386-xen_pvh/*.mod
%{_libexecdir}/i386-xen_pvh/*.module
%{_libexecdir}/i386-xen_pvh/config.h
%{_libexecdir}/i386-xen_pvh/gdb_grub
%{_libexecdir}/i386-xen_pvh/gmodule.pl
%{_libexecdir}/i386-xen_pvh/kernel.exec
%{_libexecdir}/i386-xen_pvh/kernel.img
%endif

%files mkfont
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/grub-mkfont
%{_mandir}/man1/grub-mkfont.1*

%files theme-starfield
%defattr(644,root,root,755)
%{_datadir}/grub/themes/starfield
