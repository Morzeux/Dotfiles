PS1='\[\e[0;31m\]\u@\h\[\e[m\] \[\e[1;34m\]\w\[\e[m\] \[\e[0;31m\]\$ \[\e[m\]\[\e[0;32m\]'

export PATH="$PATH:$HOME/Scripts"
export VISUAL="vim"
export LESS='-R'
export LESSOPEN='|~/.lessfilter %s'

if [ -f $HOME/.dotfiles_conf ]
then
  . $HOME/.dotfiles_conf
fi

# Shared aliases which are same for each distribution
if [ -f $HOME/.bash_aliases ]
then
  . $HOME/.bash_aliases
fi

# Aliases specific for distribution
if [ -f $HOME/.bash_aliases_ext ]
then
  . $HOME/.bash_aliases_ext
fi

# Aliases which are not synced
if [ -f $HOME/.bash_aliases_local ]
then
  . $HOME/.bash_aliases_local
fi

