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
%bcond_with	grubemu	# build grub-emu debugging utility
%bcond_without	efiemu	# build efiemu runtimes
%bcond_without	pc	# do not build for PC BIOS platform
%bcond_without	efi	# do not build for EFI platform

%if "%{cc_version}" < "3.4"
# cc does not support:
# cc1: sorry, unimplemented: code model `large' not supported yet
%undefine	with_efiemu
%endif

%ifnarch %{ix86} %{x8664}
%undefine	with_pc
%endif
%ifnarch %{ix86} %{x8664} ia64
%undefine	with_efi
%endif

%ifnarch %{x8664}
# non-x86_64 arch doesn't support this
%undefine	with_efiemu
%endif

# the 'most natural' platform should go last
%ifarch %{ix86} %{x8664} ia64
%define		platforms %{?with_efi:efi} %{?with_pc:pc}
%endif
%ifarch ppc ppc64 sparc64
%define		platforms ieee1275
%endif
%ifarch mips
%define		platforms arc
%endif
%ifarch mipsel
%define		platforms loongson
%endif

Summary:	GRand Unified Bootloader
Summary(de.UTF-8):	GRUB2 - ein Bootloader für x86 und ppc
Summary(hu.UTF-8):	GRUB2 - rendszerbetöltő x86 és ppc gépekhez
Summary(pl.UTF-8):	GRUB2 - bootloader dla x86 i ppc
Summary(pt_BR.UTF-8):	Gerenciador de inicialização GRUB2
Name:		grub2
Version:	2.00
Release:	0.9
License:	GPL v2
Group:		Base
Source0:	http://ftp.gnu.org/gnu/grub/grub-%{version}.tar.xz
# Source0-md5:	a1043102fbc7bcedbf53e7ee3d17ab91
Source1:	update-grub
Source2:	update-grub.8
Source3:	grub.sysconfig
Source4:	grub-custom.cfg
Patch1:		pld-sysconfdir.patch
Patch2:		grub-garbage.patch
Patch3:		grub-lvmdevice.patch
Patch4:		pld-mkconfigdir.patch
Patch5:		grub-mkconfig-diagnostics.patch
Patch6:		ppc.patch
Patch7:		%{name}-awk.patch
Patch8:		posix.patch
Patch9:		%{name}-gets.patch
Patch10:	%{name}-fonts_path.patch
Patch11:	%{name}-tftp_fix.patch
Patch12:	add-vlan-tag-support.patch
Patch13:	just-say-linux.patch
Patch14:	add-GRUB-DISABLE-SUBMENU-option.patch
Patch15:	add-X-option-to-printf-functions.patch
Patch16:	dhcp-client-id-and-uuid-options-added.patch
Patch17:	fix-http-crash.patch
Patch18:	Issue-separate-DNS-queries-for-ipv4-and-ipv6.patch
Patch19:	search-for-specific-config-file-for-netboot.patch
Patch20:	ignore-kernel-symlinks.patch
Patch21:	choose-preferred-initrd.patch
URL:		http://www.gnu.org/software/grub/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake >= 1:1.11.1-1
BuildRequires:	bison
BuildRequires:	device-mapper-devel
BuildRequires:	flex >= 2.5.35
BuildRequires:	fonts-TTF-DejaVu
BuildRequires:	freetype-devel >= 2
BuildRequires:	gawk
BuildRequires:	gettext-devel
BuildRequires:	glibc-static
BuildRequires:	help2man
BuildRequires:	libfuse-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	rpm >= 4.4.9-56
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
BuildRequires:	gcc-multilib
%endif
%endif
Requires:	%{name}-platform = %{version}-%{release}
Requires:	which
%ifarch %{ix86} %{x8664}
Suggests:	%{name}-platform-pc
%endif
Suggests:	cdrkit-mkisofs
Suggests:	os-prober
Provides:	bootloader
Conflicts:	grub
ExclusiveArch:	%{ix86} %{x8664} ia64 mips mipsel ppc ppc64 sparc64
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
%define		filterout_c	-fPIC
%undefine	_ssp_cflags

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
Requires:	bash-completion

%description -n bash-completion-%{name}
This package provides bash-completion for GRUB.

%description -n bash-completion-%{name} -l pl.UTF-8
Pakiet ten dostarcza bashowe uzupełnianie nazw dla GRUB-a.

%package platform-pc
Summary:	PC BIOS platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy PC BIOS dla GRUB-a
Group:		Base
Provides:	%{name}-platform = %{version}-%{release}

%description platform-pc
PC BIOS platform support for GRUB.

%description platform-pc -l pl.UTF-8
Obsługa platformy PC BIOS dla GRUB-a.

%package platform-efi
Summary:	(U)EFI platform support for GRUB
Summary(pl.UTF-8):	Obsługa platformy (U)EFI dla GRUB-a
Group:		Base
Suggests:	efibootmgr
Provides:	%{name}-platform = %{version}-%{release}

%description platform-efi
(U)EFI platform support for GRUB.

%description platform-efi -l pl.UTF-8
Obsługa platformy (U)EFI dla GRUB-a.

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
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1

%if "%{cc_version}" < "3.4"
grep -rl -- -Wno-missing-field-initializers . | xargs %{__sed} -i -e 's,-Wno-missing-field-initializers,,'
%{__sed} -i -e '/video_mod_CFLAGS/s/$/ -Wno-error/' conf/common.rmk
%endif

%build
# if gold is used then grub doesn't even boot
install -d our-ld
ln -s /usr/bin/ld.bfd our-ld/ld
export PATH=$(pwd)/our-ld:$PATH

cp -f /usr/share/automake/config.sub .
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
echo timestamp > stamp-h.in
%{__autoconf}
%{__automake}
export CFLAGS="%{rpmcflags} -Os %{?debug:-g}"

for platform in %{platforms} ; do
	install -d build-${platform}
	cd build-${platform}

	if [ "$platform" != "efi" ] ; then
		platform_opts="--enable-efiemu%{!?with_efiemu:=no}"
	else
		platform_opts=""
	fi

	ln -s ../configure .
	# mawk stalls at ./genmoddep.awk, so force gawk
	AWK=gawk \
	%configure \
		--with-platform=${platform} \
		--disable-werror \
	%if %{with grubemu}
		--enable-grub-emu-usb \
		--enable-grub-emu-sdl \
		--enable-grub-emu-pci \
	%endif
		$platform_opts \
		TARGET_LDFLAGS=-static

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
%ifnarch %{ix86} %{x8664}
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

%triggerpostun -- %{name} < 2.00-0.1
# Note this trigger on version upgrade
# needed only for upgrade from old grub2 packages
# which contained modules in /boot/grub
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
%attr(755,root,root) %{_sbindir}/grub-kbdcomp
%attr(755,root,root) %{_sbindir}/grub-install
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
%attr(755,root,root) %{_sbindir}/grub-script-check
%attr(755,root,root) %{_sbindir}/grub-set-default
%attr(755,root,root) %{_sbindir}/update-grub
%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_sbindir}/grub-bios-setup
%{_mandir}/man8/grub-bios-setup.8*
%endif
%ifarch %{ix86} %{x8664}
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
%{_mandir}/man1/grub-fstest.1*
%{_mandir}/man1/grub-kbdcomp.1*
%{_mandir}/man1/grub-menulst2cfg.1*
%{_mandir}/man1/grub-mklayout.1*
%{_mandir}/man1/grub-mkpasswd-pbkdf2.1*
%{_mandir}/man1/grub-mkrelpath.1*
%{_mandir}/man1/grub-mkrescue.1*
%{_mandir}/man1/grub-mkstandalone.1*
%{_mandir}/man1/grub-mount.1*
%{_mandir}/man1/grub-script-check.1*
%{_mandir}/man8/grub-install.8*
%{_mandir}/man8/grub-mkconfig.8*
%{_mandir}/man8/grub-mknetdir.8*
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

%ifarch %{ix86} %{x8664}
%attr(755,root,root) %{_sbindir}/grub-probe
%{_mandir}/man8/grub-probe.8*
%endif

%{_infodir}/grub*.info*

%dir %{_datadir}/grub/themes

%if %{with pc}
%files platform-pc
%defattr(644,root,root,755)
%dir %{_libexecdir}/*-pc
%{_libexecdir}/*-pc/modinfo.sh
%{_libexecdir}/*-pc/*.exec
%{_libexecdir}/*-pc/*.image
%{_libexecdir}/*-pc/*.lst
%{_libexecdir}/*-pc/*.mod
%{_libexecdir}/*-pc/*.module
%{_libexecdir}/*-pc/lzma_decompress.img
%{_libexecdir}/*-pc/config.h
%{_libexecdir}/*-pc/gdb_grub
%{_libexecdir}/*-pc/gmodule.pl
%if %{with efiemu}
%{_libexecdir}/*-pc/efiemu*.o
%endif
%{_libexecdir}/*-pc/kernel.img
%ifarch %{ix86} %{x8664} sparc sparc64
%{_libexecdir}/*-pc/boot.img
%{_libexecdir}/*-pc/cdboot.img
%{_libexecdir}/*-pc/diskboot.img
%{_libexecdir}/*-pc/lnxboot.img
%{_libexecdir}/*-pc/pxeboot.img
%endif
%endif

%if %{with efi}
%files platform-efi
%defattr(644,root,root,755)
%dir %{_libexecdir}/*-efi
%{_libexecdir}/*-efi/modinfo.sh
%{_libexecdir}/*-efi/*.exec
%{_libexecdir}/*-efi/*.lst
%{_libexecdir}/*-efi/*.mod
%{_libexecdir}/*-efi/*.module
%{_libexecdir}/*-efi/config.h
%{_libexecdir}/*-efi/gdb_grub
%{_libexecdir}/*-efi/gmodule.pl
%{_libexecdir}/*-efi/kernel.img
%endif

%files mkfont
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/grub-mkfont
%{_mandir}/man1/grub-mkfont.1*

%files theme-starfield
%defattr(644,root,root,755)
%{_datadir}/grub/themes/starfield

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
/etc/bash_completion.d/grub
