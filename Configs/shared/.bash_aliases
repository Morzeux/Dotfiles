#!/bin/bash

# reusable aliases
alias ls='ls --color=auto'
alias ..='cd ..'
alias dp-project='source ~/storage_linux/venv/py35-dp-project/bin/activate'
alias dp-project-27='source ~/storage_linux/venv/py27-dp-project/bin/activate'
alias workspace='cd ~/workspace/projects/python'
alias devel-on='sudo devel-on'
alias cls='clear'
alias starwars='telnet towel.blinkenlights.nl'
alias diskspace='du -S | sort -n -r | less'
alias lsless='ls --color=always -al | less -R'i
alias su='toilet "With great power comes great responsibility!" -t  -f future; su'
alias aqua='asciiquarium'
alias dconf-store='rm -f $DOTFILES_PATH/Configs/dconf_backup.dconf; dconf dump / > $DOTFILES_PATH/Configs/dconf_backup.dconf'
alias dconf-loads='dconf load / < $DOTFILES_PATH/Configs/dconf_backup.dconf'