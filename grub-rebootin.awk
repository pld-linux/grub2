#!/bin/awk -f

BEGIN {
	menu = "/boot/grub/menu.lst"
	once = "/boot/grub/menu.once"

	if ((getline < menu) > 0)
		close(menu)
	else {
		print "grub is not installed (" menu " is missing)"
		exit 1
	}
	nrentries = 0
	altconfig = 0
	while (getline < menu) {
		if ( /^title[ \t]+/ ) {
			gsub(/^title[ \t]+/,"")
			entries[nrentries] = $0
			nrentries++
		}
		if ( /^altconfigfile[ \t]+.*grub\/menu\.once/ )
			altconfig = 1
	}
	if ( !altconfig ) {
		print "rebootin is of no use without altconfigfile"
		exit 2
	}
	if ( !nrentries ) {
		print "bad menu.lst (no entry found)"
		exit 3
	}
	if ( ARGC != 2 ) {
		print "usage: rebootin <label>\n  where <label> is one of "
		for (n = 0 ; n < nrentries ; n++)
			print "	" entries[n]
		exit 4
	}

	for (n = 0 ; n < nrentries ; n++)
		if ( ARGV[1] == entries[n] ) {
			dflt = "default " n
			print dflt "\ntimeout 0\n" > once
			close(once)
			getline be_safe < once
			if ( be_safe != dflt ) {
				print "can't write rebootin file (" once "), verify the rights"
				exit 666
			}
			system("/sbin/shutdown -r now")
			print "dupa"
		}

	print "\"" ARGV[1] "\" not found"
}
