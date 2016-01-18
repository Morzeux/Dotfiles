# Install Guide

This guide may not be perfect and may contains some misleading. These commands worked very well on Virtualbox machine under my Lenovo Thinkpad e540 laptop, however it may not be suitable on different setup. It serves primary for inspiration. I will try to point in parts which can be different. As the result Cinnamon 3D desktop environment with was configured with some basic desktop apps.

## Gentoo Base Install

This covers procedure between live CD is booted and base runnable Gentoo is configured. I highly recommend to follow [Gentoo Handbook](https://wiki.gentoo.org/wiki/Handbook:Main_Page) and use this as inspiration. In this setup I'm using systemd instead of update-rc.

### Preparations

This covers partitioning, downloading *stage3* tarball and basic compile configuration.

#### Network pre-configuration
```
$ net-setup INTERFACE
$ dhcpcd INTERFACE
```

And check:
```
$ ping google.com
```

#### Partitioning

This partitioning covers GPT without EFI (is enough for Virtualbox).

Check physical drives:
```
$ lsblk
```

Pick one (mine is /dev/sda)
```
$ parted /dev/sda
```

My setup will be 2MB for *GRUB* partition, 512MB *BOOT* partition, 2GB *SWAP* partition and rest *ROOT* partition.
```
(parted) $ mklabel gtp
(parted) $ mklabel gtp
(parted) $ mklabel gtp
(parted) $ mklabel gtp
```
