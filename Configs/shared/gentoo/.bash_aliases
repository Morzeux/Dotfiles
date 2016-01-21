#!/bin/bash
alias pclean='sudo emerge --depclean'
alias pupdate='sudo layman -S && sudo emerge --sync && sudo eix-update && sudo emerge -uDN @world && pclean'
alias pbackup='sudo cp /etc/portage/package* $DOTFILES_PATH/System/gentoo/portage/;sudo cp /etc/portage/make.conf $DOTFILES_PATH/System/gentoo/portage/;sudo cp /var/lib/layman/make.conf $DOTFILES_PATH/System/gentoo/layman/; sudo cp /usr/src/linux/.config $DOTFILES_PATH/System/gentoo/.kernel_config'
