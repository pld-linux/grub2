# grub driver for rc-boot

LOADER_CONFIG=/boot/grub/menu.lst


GRUB_Root_convert() 	# This function simply converts the normal Linux
		    	# device name into the form (MajorMinornumber)
			# it is neccesary becouse the bug in grub.
{
	ls -l $1 | awk '{gsub(/,/,"",$5); printf "%04x", $5*256+$6}'
}


# BIG FAT WARNING: this function ain't very bright... it will fail in variety
# of situation including (but by no means limited to) having IDE and
# SCSI drives on the same machine (and BIOS numbers first devices
# you're not booting from), booting from second hardware RAID, and so on.

GRUB_convert()		# This function converts the normal Linux 
			# device name into the stupid grub notation 
			# for example /dev/hda2 = (hd0,2)
{
	GROOT=`basename $1`
 
	GROOT=`echo $GROOT| awk '{sub(/^hd|^sd|^c[0-9]d/,"");print $0}'` 
	if echo $GROOT | grep -q '^[0-9][0-9]*$' ; then
		DRIVE=$GROOT
	else
		DRIVE=`echo $GROOT| awk '{sub(/p?[0-9]*$/,"");print $0}'`
	fi
	NR=`echo $GROOT| awk '{sub(/^([a-z]*|[0-9]*p?)/,"");print $0}'`
	NDRIVE=""
		
	if echo $DRIVE | grep -q '^[0-9][0-9]*$' ; then
		NDRIVE=$DRIVE
	else
		TR=`echo $DRIVE |tr "a-j" "0-9"`
		[ "${DRIVE}" != "$TR" ] && NDRIVE="$TR"
		TR=`echo $DRIVE |tr "k-u" "0-9"`
		[ "${DRIVE}" != "$TR" ] && NDRIVE="1${TR}"
		TR=`echo $DRIVE |tr "w-z" "0-3"`
		[ "${DRIVE}" != "$TR" ] && NDRIVE="2${TR}"
	fi
	
	if [ "${NDRIVE}" = "" ]; then
		rcboot_message "Error in \"$CONFIG_DIR/images/$NAME\" file improper ROOT option"
		exit 1
	fi
	if [ "${NR}" != "" ]; then 
		NR=`expr $NR - 1`
		echo "(hd${NDRIVE},$NR)"
	else
		echo "(hd${NDRIVE})"
	fi
	unset TR NR NDRIVE GROOT DRIVE
}

GRUB_COUNTER=0
GRUB_DEF=0
GRUB_FALL=1

rc_boot_prep_image () {
	if [ "$LILO_ONLY" != "" ] && is_yes "$LILO_ONLY" ; then 
		return 0
	fi
  
	if [ "$NAME" = "$DEFAULT" ] ; then
		GRUB_DEF=$GRUB_COUNTER
	fi

	if [ "$NAME" = "$FALLBACK" ]; then
		GRUB_FALL=$GRUB_COUNTER
	fi
	
	GRUB_COUNTER=$(($GRUB_COUNTER+1))
}

rc_boot_init () {
	[ "$COLORS" = "" ] && COLORS="white/blue blue/white"

	if [ -z "$FALBACK" ]; then
		FALLBACK="second";
	fi
  
	# This is the main part of the /boot/grub/menu.lst
	cat <<!EOF!
# By default boot the $DEFAULT entry
default $GRUB_DEF
# Wait $TIMEOUT seconds for booting
timeout $TIMEOUT
# Fallback to the $FALLBACK entry if default fails
fallback $GRUB_FALL
# Default colors
color $GRUB_COLORS
!EOF!

	if [ "$PASSWORD" != "" ] ; then 
		echo "#The password:"
		echo "password $PASSWORD"
	fi
}

GRUB_SEPARATE_BOOT=unknown

strip_boot () {
  case $GRUB_SEPARATE_BOOT in
    yes )
      INITRD=$(echo $INITRD | sed -e 's|/boot||')
      KERNEL=$(echo $KERNEL | sed -e 's|/boot||')
      ;;
    no )
      ;;
    * )
      boot=$(get_dev /boot)
      root=$(get_dev /)
      if [ "$boot" != "" -a "$root" != "$boot" ] ; then
        debug "separate boot = yes"
        GRUB_SEPARATE_BOOT=yes
      else
        debug "separate boot = no"
        GRUB_SEPARATE_BOOT=no
      fi
      strip_boot
      ;;
  esac
}

rc_boot_image () {
	if [ "$LILO_ONLY" != "" ] && is_yes "$LILO_ONLY" ; then 
		return 0
	fi

	echo "# $TYPE image"
	if [ "${TITLE}" ]; then
		echo "title $TITLE"
	else
		echo "title $NAME"
	fi
	if is_yes "$LOCK" ; then
		echo "lock"
	fi

	strip_boot
  
	case "$TYPE" in
	linux )
		ROOT="root=$(GRUB_Root_convert $ROOT)"
		[ "${VGA}" != "" ] && VGA="vga=${VGA}"
		echo kernel "$KERNEL" "$ROOT" "$VGA" "${APPEND}"
		[ "$INITRD" != "" ] && echo "initrd $INITRD"
		;;
	dos | bsd )
		echo "root $(GRUB_convert $ROOT)"
		echo "makeactive"
		echo "chainloader +1"
		;;
	*)	# Buuu 
		die "Don't know how to handle OS type = '$TYPE'"
		;;
	esac
}

rc_boot_fini () {
	echo "# EOF"
}

rc_boot_run () {
	if [ "$GRUB_SEPARATE_BOOT" = yes ] ; then
		# nasty workaround :<<
		mkdir -p /boot/boot/grub || die "cannot create /boot/boot/grub"
		rm -f /boot/boot/grub/menu.lst
		ln /boot/grub/menu.lst /boot/boot/grub/menu.lst

		# this is not part of workaround :^)
		grubdir=/grub
	else
		grubdir=/boot/grub
	fi

	root_drive=$(GRUB_convert $STAGE2)
	install_drive=$(GRUB_convert $BOOT)
  
	debug "root_drive = $root_drive [$STAGE2]"
	debug "install_drive = $install_drive [$BOOT]"
  
	log=`mktemp /tmp/grub.XXXXXX`
	/sbin/grub --batch > $log 2>&1 <<EOF
root $root_drive
setup --stage2=/boot/grub/stage2 --prefix=$grubdir $install_drive
quit
EOF

	if grep -q "Error [0-9]*: " $log ; then
		while read LINE ; do
		msg "grub: $LINE"
		done < $log
		die "grub failed"
	fi

	while read LINE ; do
		debug "grub: $LINE"
	done < $log
  
	rm -f $log
  
	#/sbin/grub-install $BOOT >/dev/null 2>&1
}

# Thats all folk.
