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

```
Gentoo Linux --->
  Support for init systems, system and service managers --->
    [*] systemd

General setup  --->
  (-morzeux) Local version - append to kernel release
  -*- open by fhandle syscalls
  -*- Control Group support
  [*] Namespaces support  --->
    -*- Network namespace
  [ ] Enable deprecated sysfs features to support old userspace tools
  [*] Configure standard kernel features (expert users)  --->
    -*- Enable eventpoll support
    -*- Enable signalfd() system call
    -*- Enable timerfd() system call

-*- Enable the block layer  --->
  [*] Block layer SG support v4
  Partition Types --->
    [*] Advanced partition selection
      [*] EFI GUID Partition support

Processor type and features  --->
  [*] Symmetric multi-processing support
  [*] Enable seccomp to safely compute untrusted bytecode

Executable file formats / Emulations  --->
   [*] IA32 Emulation

-*- Networking support --->
  Networking options --->
    <*> The IPv6 protocol

Device drivers -->
  Generic Driver Options  --->
    ()  path to uevent helper
    -*- Maintain a devtmpfs filesystem to mount at /dev
    [ ]   Automount devtmpfs at /dev, after the kernel mounted the rootfs
    [ ] Fallback user-helper invocation for firmware loading
  Input Device Support --->
    <*> Event Interface
  Character devices --->
    [*] Support multiple instances of devpts
  Graphics support -->
    [*] Laptop Hybrid Graphics - GPU switching support
    Direct Rendering Manager -->
      <*> Direct Rendering Manager(XFree86 and higher DRI support) --->
        <M> Intel 8xx/9xx/G3x/G4x/HD Graphics
          [*] Enable modesetting on intel by default
    <*> Support for frame buffer devices --->
      -*-   Enable Video Mode Handling Helpers
      [ ]   Enable Tile Blitting Support
    Console display driver support --->
      [*] VGA text console
      [*]   Enable Scrollback Buffer in System RAM
      (64)    Scrollback Buffer Size (in KB)
      <*> Framebuffer Console support
      [*]   Map the console to the primary display device
      [ ]   Framebuffer Console Rotation
      [*]   Support for the Framebuffer Console Decorations
      [ ] Select compiled-in fonts
    [*] Bootup logo
      [x] Standard 224-color Linux logo

Firmware Drivers  --->
  [*] Export DMI identification via sysfs to userspace

File systems --->
  <*> Second extended fs support
  <*> Ext3 journalling file system support
  <*> The Extended 4 (ext4) filesystem
  <*> Reiserfs support
  <*> JFS filesystem support
  <*> XFS filesystem support
  -*- Inotify support for userspace
  -*- Kernel automounter version 4 support (also supports v3)
  ...
  Pseudo Filesystems --->
    -*- /proc file system support
    -*- sysfs file system support
    -*- Tmpfs virtual memory file system support (former shm fs)
    [*]   Tmpfs POSIX Access Control Lists
    -*-   Tmpfs extended attributes
```

Save, exit and wait for compilation to be finished. After compiling built external modules:
```
$ cd /usr/src/linux
$ make modules_prepare
$ emerge -a @module-rebuild
```

Now write:
```
$ ln -sf /proc/self/mounts /etc/mtab
```

And download firmware and network support:
```
$ emerge -a sys-kernel/linux-firmware
$ emerge -a net-misc/networkmanager enet-misc/dhcpcd
```

#### Bootloader setup

Finally we are going to configure grub bootloader and reboot to newly installed system. So firstly install grub bootloader. If you are using EFI, then add *GRUB_PLATFORMS="efi-64"* to make.conf:

```
$ emerge -a sys-boot/grub
```

And install grub:
```
$ grub2-install /dev/sda
```

If you are using EFI:
```
$ grub2-install --target=x86_64-efi --efi-directory=/boot
```

Using nano uncomment line *GRUB_CMDLINE_LINUX="init=/usr/lib/systemd/systemd*:
```
$ nano -w /etc/default/grub
```

And update configuration:
```
$ grub2-mkconfig -o /boot/grub/grub.cfg
```

Now you should have installed base system. Rest is up to unchroot and reboot:
```
$ exit
(livecd) $ umount -l /mnt/gentoo/dev{/shm,/pts,}
(livecd) $ umount /mnt/gentoo{/boot,/sys,/proc,}
```

Take a deep breath and reboot:
```
(livecd) $ reboot
```

### Post-installation configurations

If all went well, then you should boot into freshly installed Gentoo system. Now we are going to install some services and cleanup unnecessary install files.

Firstly setup hostname and locales:

```
$ hostnamectl set-hostname HOSTNAME
$ localectl set-locale LANG="en_US.utf8"
$ timedatectl set-timezone Europe/Bratislava
```

Then enable network services:
```
$ systemctl enable NetworkManager.service
$ systemctl start NetworkManager.service
$ systemctl enable dhcpcd.service
$ systemctl start dhcpcd.service
$ ping google.com
```

And finally install some useful services:
```
$ emerge -a net-misc/ntp
$ emerge -a app-admin/syslog-ng
$ emerge -a sys-process/cronie
$ emerge -a sys-apps/mlocate
$ emerge -a sys-fs/dosfstools
$ emerge -a sys-apps/pciutils
$ systemctl enable ntpd.service
$ systemctl enable syslog-ng.service
$ systemctl enable cronie.service
$ systemctl enable sshd.service
```

Now configure *vim* as default editor instead of nano:
```
$ emerge -a app-editors/vim
$ eselect editor list
$ eselect editor set N
```

Add some regular user and allow him to sudo:
```
$ emerge -a sys-admin/sudo
$ useradd -m -G users,wheel,audio,video,cdrom,usb -s /bin/bash USERNAME
$ passwd USERNAME
$ vim /etc/sudoers
```

Then uncomment line *%wheel ALL=(ALL) ALL* and save.

Finally cleanup unnecessary stage3 install file and reboot:
```
$ rm /stage3-amd64-*
$ reboot
```

You should now to have installed and configured basic system.

## Gentoo Tweaking

At this part we are going to install and configure some Gentoo tweak as sound, gui, splashscreen, themes and my dotfiles.

### Sound

I advice to look at [PulseAudio](https://wiki.gentoo.org/wiki/ALSA and https://wiki.gentoo.org/wiki/PulseAudio) page first and configure your kernel according to your needs.

Firstly login as user and install alsa-utils:
```
(user) $ sudo emerge -a alsa-utils
```

Then unmute and configure volume and finally test it:
```
(user) $ alsamixer
(user) $ speaker-test -t wav -c 2
```

Finally install pulseautio with pavucontrol:
```
(user) $ sudo emerge -a media-plugins/alsa-plugins media-sound/pulseaudio media-sound/pavucontrol
```

### Xorg Server

First I advice to read [Xorg](https://wiki.gentoo.org/wiki/Xorg/Guide) and [Xorg Server](https://wiki.gentoo.org/wiki/X_server) guides. After check that display drivers are correctly set continue:

```
$ emerge -a x11-base/xorg-drivers x11-base/xorg-server xterm twm
$ env-update
$ source /etc/profile
$ startx
```

You should now see basic Xorg gui interface.

#### Cinnamon and Desktop Manager

To install Cinnamon firstly emerge gtk-extra:

```
$ emerge -a x11-libs/gtk+extra
```

Then proceed with Cinnamon, don't forget to grab a large cup of coffee:
```
$ emerge -a gnome-extra/cinnamon x11-terms/gnome-terminal
$ emerge -a media-libs/gst-plugins-good media-plugins/gst-plugins-vpx
```

As user setup your cinnamon session and start:
```
(user) $ echo "exec cinnamon-session" > .xinitrc
(user) $ startx
```

You should see basic Cinnamon GUI, now it is time to configure desktop manager. I'm using Slim.
```
$ emerge -a x11-misc/slim
$ systemctl enable slim.service
```

Finally edit */etc/slim.conf* and:
```
comment out *# login_cmd exec /bin/bash -login /usr/share/slim/Xsession %session*
uncommnet *login_cmd exec /bin/bash -login ~/.xinitrc %session*
set *defaultuser USERNAME*
```

And finally reboot:
```
$ reboot
```

You should now boot to Cinnamon desktop. You can now install some useful apps:

```
$ emerge -a gnome-extra/gnome-calculator media-gfx/gnome-screenshot media-gfx/eog app-text/evince
$ emerge -a gnome-extra/gnome-system-monitor app-arch/file-roller app-cdr/brasero app-editors/gedit
$ emerge -a www-client/firefox
```

#### Beauty fonts

I took an inspiration from this [guide](http://kev009.com/wp/2009/12/getting-beautiful-fonts-in-gentoo-linux/). So firstly install som cool fonts:

```
$ emerge -a app-eselect/eselect-fontconfig media-fonts/corefonts media-fonts/dejavu media-fonts/font-bh-ttf media-fonts/font-bh-type1 media-fonts/freefonts media-fonts/ttf-bitstream-vera media-fonts/unifont media-fonts/artwiz-aleczapka-en media-fonts/ubuntu-font-family
```

And then turn on these fonts:
```
10-autohint.conf
10-sub-pixel-rgb.conf
20-unhint-small-dejavu-sans-mono.conf
20-unhint-small-dejavu-sans.conf
20-unhint-small-dejavu-serif.conf
25-unhint-nonlatin.conf
57-dejavu-sans-mono.conf
57-dejavu-sans.conf
57-dejavu-serif.conf
```

Using commands:
```
$ eselect fontconfig list
$ eselect fontconfig set N
```

#### Portage tools and Layman

There are several useful portage tools:

```
$ emerge -a app-portage/gentoolkit app-portage/cfg-update app-portage/eix dev-util/meld
$ emerge -a app-portage/layman
```

And configure Layman:
```
$ layman -L
$ echo "source /var/lib/layman/make.conf" >> /etc/portage/make.conf
$ eix-update
```

#### Splashscreen

In this part we will install some Gentoo splashscreen with framebuffer.

```
$ emerge -a splashutils media-gfx/splash-themes-gentoo
```

Now edit grub config */etc/default/grub* and set this line:
```
RUB_CMDLINE_LINUX_DEFAULT="linux video=uvesafb:1024x768-32,mtrr:3,ywrap 
```

Also edit */etc/genkernel.conf* and set these lines:
```
SPLASH="yes"
SPLASH_THEME="natural_gentoo"
```

Finally update grub config and rebuild kernel:
```
$ grub2-mkconfig -o /boot/grub/grub.cfg
$ cd /usr/src/linux
$ genkernel --no-clean all
$ make modules_prepare
$ emerge -a @module-rebuild
```

Finally reboot with new splash screen:
```
$ reboot
```

#### Grub theming

In this part we will add cutom grub theme. Firstly add new layer to layman and install new theme:
```
$ layman -a grub2-themes
$ emerge -a grub2-themes/steam-big-picture
$ cp -r /usr/share/grub/themes/steam-big-picture /boot/grub/themes/steam-big-picture
```

Now edit */etc/default/vim* and set these lines:
```
GRUB_GFXMODE=1024x768
GRUB_THEME="/boot/grub/themes/steam-big-picture/theme.txt"
```

Finally update grub and reboot:
```
$ grub2-mkconfig -o /boot/grub/grub.cfg
$ reboot
```
