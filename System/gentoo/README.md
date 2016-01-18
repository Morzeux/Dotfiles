# Install guide

This guide may not be perfect and may contains some misleading. These commands worked very well on Virtualbox machine under my Lenovo Thinkpad e540 laptop, however it may not be suitable on different setup. It serves primary for inspiration. I will try to point in parts which can be different. As the result Cinnamon 3D desktop environment with was configured with some basic desktop apps.

## Gentoo base install

This covers procedure between live CD is booted and base runnable Gentoo is configured. I highly recommend to follow [Gentoo Handbook](https://wiki.gentoo.org/wiki/Handbook:Main_Page) and use this as inspiration. In this setup I'm using systemd instead of update-rc.

### Preparations

This covers partitioning, downloading *stage3* tarball until chrooting into system.

#### Network pre-configuration
```
(livecd) $ net-setup INTERFACE
(livecd) $ dhcpcd INTERFACE
```

And check:
```
(livecd) $ ping google.com
```

#### Partitioning

This partitioning covers GPT without EFI (is enough for Virtualbox).

Check physical drives:
```
(livecd) $ lsblk
```

Pick one (mine is /dev/sda)
```
(livecd) $ parted /dev/sda
```

My setup will be 2MB for *GRUB* partition, 512MB *BOOT* partition, 2GB *SWAP* partition and rest *ROOT* partition.
```
(parted) $ mklabel gtp
(parted) $ unit mib
(parted) $ mkpart primary 1 3
(parted) $ name 1 grub
(parted) $ set 1 bios_grup on
(parted) $ 
(parted) $ mkpart primary 3 515
(parted) $ name 2 boot
(parted) $ set 2 boot on
(parted) $ 
(parted) $ mkpart primary 515 2563
(parted) $ name 3 swap
(parted) $ 
(parted) $ mkpart primary 2563 -l
(parted) $ name 4 rootfs
(parted) $
(parted) $ quit
```

Now format and mount them:
```
(livecd) $ mkfs.ext2 /dev/sda2
(livecd) $ mkswap /dev/sda3; swapon /dev/sda3
(livecd) $ mkfs.ext4 /dev/sda4
(livecd) $
(livecd) $ mount /dev/sda4 /mnt/gentoo
(livecd) $ mkdir -p /mnt/gentoo/boot
(livecd) $ mount /dev/sda2 /mnt/gentoo/boot
```

#### Download Stage3 tarball

This part is about downloading, verifying and unpacking stage3 tarball.

Download current release from:
```
(livecd) $ links https://www.gentoo.org/downloads/mirrors/
```

Now verify signature and checksum:
```
(livecd) $ openssl dgst -r -sha512 stage3-<release>.tar.bz2
(livecd) $ zless stage3-<release>.tar.bz2.DIGESTS.bz2
(livecd) $ gpg --verify stage3-<release>.tar.bz2.DIGESTS.asc
```

And unpack:
```
(livecd) $ tar xvjpf stage3-*.tar.bz2 --xattrs
```

#### Chrooting

Now we are going to chroot to new Gentoo system.

First:
```
(livecd) $ cp -L /etc/resolv.conf /mnt/gentoo/etc/
```

And secondly mount:
```
(livecd) $ mount -t proc proc /mnt/gentoo/proc
(livecd) $ mount --rbind /sys /mnt/gentoo/sys
(livecd) $ mount --make-rslave /mnt/gentoo/sys
(livecd) $ mount --rbind /dev /mnt/gentoo/dev
(livecd) $ mount --make-rslave /mnt/gentoo/dev
```

And finally chroot:
```
(livecd) $ chroot /mnt/gentoo /bin/bash
$ source /etc/profile
```

Don't forget to set root's password after successful chroot:
```
$ passwd PASSWORD
```

### Installation

This covers base compilling configurations, kernel compilation and then its installation.

#### Portage

This covers configuration and installation package manager *portage*. **Caution** here, these compile flags are suitable for my platform, however may not be suitable on different platform. Useful resources I strongly recommends to read first:
* [Safe CFLAGS](https://wiki.gentoo.org/wiki/Safe_CFLAGS)
* [GCC optimization](https://wiki.gentoo.org/wiki/GCC_optimization)

Edit make.conf and configure *make.conf* file. [This one](https://github.com/Morzeux/Dotfiles/blob/master/System/gentoo/portage/make.conf) is mine.
```
$ nano -w /etc/portage/make.conf
```

Now it is time to configure current time. To check if date is current:
```
$ date
```

And eventually configure:
```
$ date MMDDhhmmYYYY
```

Now you can synchronize *portage*:
```
$ emerge-webrsync
$ emerge --sync
```

Now selects your favorite *profile*, where *X* is profile number. Mine is */amd64/13.0/desktop/gnome/systemd*:
```
$ eselect profile list
$ eselect set X
```

Now update your packages. You will have to remove *sys-fs/udev* as this is blocking package for *systemd*. And... take a cup of coffee.
```
$ emerge -C sys-fs/udev
$ emerge -uDNa @world
```

#### Locales

This part describes base locale configuration.

Starting with timezone:
```
$ echo "Europe/Bratislava" > /etc/timezone
$ emerge --config sys-libs/timezone-data
```

Then uncomment line *en_US.UTF-8 UTF-8* using *nano*:
```
$ nano -w /etc/locale.gen
```

And finally sets locale where *N* is number for *UTF-8*:
```
$ locale-gen
$ eselect locale list
$ eselect locale set N 
$ env-update && source /etc/profile
```

#### Compilling kernel

***Caution!!*** This is most important part for configuration. This kernel configuration suites for my Intel procesor un my lenovo laptop and for my virtualbox graphics card. Also I made here some preparements for sound and flashscreen. These are sources I used for this config:
* [Lenovo Thinkpad E540](https://wiki.gentoo.org/wiki/Lenovo_Thinkpad_E540)
* [Virtualbox Guest](http://gentoo-en.vfose.ru/wiki/Virtualbox_Guest)
* [Systemd](https://wiki.gentoo.org/wiki/Systemd)
* [Fbsplash](https://wiki.gentoo.org/wiki/Fbsplash)
* [Alsa audio](https://wiki.gentoo.org/wiki/ALSA)
* [Pulseaudio](https://wiki.gentoo.org/wiki/PulseAudio)

And also don't miss [Kernel configuration guide](https://wiki.gentoo.org/wiki/Kernel/Gentoo_Kernel_Configuration_Guide).

First download *gentoo-sources* and *genkernel-next*:
```
$ emerge -a sys-kernel/gentoo-sources
$ emerge -a sys-kernel/genkernel-next
```

Then configure partitions:
```
$ nano -w /etc/fstab
```

And uncomment line *UDEV="yes"* through *nano*:
```
$ nano -w /etc/genkernel.conf
```

And finally we are going to configure kernel. Don't forget to store your configuration.
```
$ genkernel --menuconfig all
```

**To be continued...**
