# Install guide

Install guide for my Arch Linux system.

## Arch base install

This covers procedure between live CD is booted and base runnable Arch is configured. I highly recommend to follow [Beginner's Guide](https://wiki.archlinux.org/index.php/beginners'_guide) and use this as inspiration.

### Preparations

This covers base partitioning.

#### Network pre-configuration

Wireless:
```
(livecd) $ ifconfig
(livecd) $ wifi-menu -o INTERFACE
```

And check:
```
(livecd) $ ping google.com
```

#### Partitioning

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
(parted) $ mklabel gpt
(parted) $ unit mib
(parted) $ mkpart primary 1 3
(parted) $ name 1 grub
(parted) $ set 1 bios_grub on
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
(livecd) $ mount /dev/sda4 /mnt
(livecd) $ mkdir -p /mnt/boot
(livecd) $ mount /dev/sda2 /mnt/boot
```

### Installation

After partitions are mounted and prepared, install base system:

```
(livecd) $ pacstrap -i /mnt base base-devel
```

Then confirm default packages and wait until finished.

Now generate fstab and chroot:
```
(livecd) $ genfstab -U -p /mnt >> /mnt/etc/fstab
(livecd) $ arch-chroot /mnt /bin/bash
```

### Configurations

After chrooting you are ready to configure base system. First start with user configurations:

```
$ passwd
$ useradd -m -G users,wheel,audio,video -s /bin/bash USERNAME
$ passwd USERNAME
$ nano -w /etc/sudoers
```

Then uncomment line *%wheel ALL=(ALL) ALL* and save.

Now configure locales. First:
```
$ nano /etc/locale.gen
```

Then uncomment line *en_US.UTF-8 UTF-8*. Finally generate locales:

```
$ locale-gen
```

Now configure timezone and set hwclock:
```
$ ln -s /usr/share/zoneinfo/Europe/Bratislava /etc/localtime
$ hwclock --systohc --utc
```

Update hostname:
```
$ echo HOSTNAME > /etc/hostname
```

And install network:
```
$ pacman -Syu networkmanager dhcpcd dialog
```

Finally install bootloader:
```
$ mkinitcpio -p linux
$ pacman -S grub
$ grub-install --recheck /dev/sda
$ grub-mkconfig -o /boot/grub/grub.cfg
```

And reboot:
```
$ exit
$ reboot
```

### Post-installation configurations

You should now be booted in fresh installed Arch linux. There are still few things need to do.

Starting with network. Enable network services:
```
$ systemctl enable NetworkManager.service
$ systemctl enable dhcpcd.service
$ systemctl start NetworkManager.service
$ systemctl start dhcpcd.service
```

And then configure  locales:

```
$ localectl set-locale LANG="en_US.UTF-8"
```

Finally update all packages:
```
$ pacman -Syu
```

## Arch Tweaks

You should now have installed fresh system. Next step is to change console system into nice GUI system.

### Sound

To configure sound first install alsa-utils:

```
$ pacman -Syu alsa-utils
```

And then configure them as user:
```
(user) $ alsamixer
(user) $ speaker-test -c 2
```

Finally install *pulseaudio* with *pavucontrol*:
```
$ pacman -Syu pulseaudio pavucontrol
```

Choose your driver and install.

### Cinnamon with Desktop Manager

To install Cinnamon you will have to start with Xorg server first and then evaluate.

```
$ pacman -S xorg xorg-xinit xterm
$ startx
```

Now as user install Cinnamon and configure *.xinitrc*:
```
(user) $ pacman -S cinnamon gnome-terminal
(user) $ echo "exec cinnamon-session" > .xinitrc
(user) startx
```

Now install desktop manager and reboot:
```
$ pacman -S slim archlinux-themes-slim
$ systemctl enable slim.service
$ nano -w /etc/slim.conf
$ reboot
```

Install now some useful stuff.

Fonts:
```
$ pacman -Syu ttf-dejavu ttf-droid ttf-liberation ttf-ubuntu-font-family cairo # fonts
```

Codecs:
```
$ pacman -S a52dec faac faad2 flac jasper lame libdca libdv libmad libmpeg2 libtheora libvorbis libxv wavpack x264 xvidcore gstreamer0.10-plugins
```

Apps:
```
$ pacman -S firefox flashplugin vlc chromium unzip unrar p7zip pidgin skype deluge smplayer audacious qmmp gimp xfburn thunderbird gedit gnome-system-monitor libreoffice
```

### Other usefull stuff

```
$ pacman -Syu vim wget subversion git meld tor ufw gufw
```

Enabling firewall:
```
$ ufw enable
```

Installing yaourt:
```
$ pacman -S yajl
$ wget https://aur.archlinux.org/cgit/aur.git/snapshot/package-query.tar.gz
$ tar -xvf package-query.tar.gz
$ cd package-query
$ makepkg
$ pacman -U package-query-1.7-1-x86_64.pkg.tar.xz
$ cd ..
$ wget https://aur.archlinux.org/cgit/aur.git/snapshot/yaourt.tar.gz
$ tar -xvf yaourt.tar.gz
$ cd yaourt
$ makepkg
$ pacman -U yaourt-1.7-1-any.pkg.tar.xz
$ pacman -S rsync
$ cd ..
$ rm -r package-query*
$ rm -r yaourt*
```

Sublime:
```
$ yaourt -Syuab sublime-text
```
