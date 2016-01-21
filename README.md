# Dotfiles
My personal dotfiles and configurations for my installed Arch and Gentoo distributions.

Gentoo config is for my Virtualboxed Gentoo which is hosted in my Lenovo E540 Laptop.

![alt text](https://github.com/Morzeux/Dotfiles/blob/master/preview.png "Gentoo Preview")

## Install

To install:
```
$ git clone https://github.com/Morzeux/Dotfiles.git
$ python Dotfiles/install.py
```

With verbose output:
```
$ python Dotfiles/install.py -v
```

Install root configurations:
```
$ sudo python Dotfiles/install.py -r
```

This will create symbolic links pointed to directory *Configs* and *Scripts*. If these files already exists, then script will not ovveride and wil terminate instead. In order to force override them:
With verbose output:
```
$ python Dotfiles/install.py -f
```

This will forcely replace existing files with symlinks pointed to repository.

#### Loading GUI settings

After symlinks are created and .bash_aliases loaded, use alias:
```
$ dconf-loads
```

To store GUI configuration use.
```
$ dconf-store
```
