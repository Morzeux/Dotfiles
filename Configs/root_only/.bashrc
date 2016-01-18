PS1='\[\e[0;31m\]\u\[\e[m\] \[\e[1;34m\]\w\[\e[m\] \[\e[0;31m\]\$ \[\e[m\]\[\e[0;32m\]'

export PATH="$PATH:$HOME/Scripts"
export VISUAL="vim"
export LESS='-R'
export LESSOPEN='|~/.lessfilter %s'

if [ -f $HOME/.dotfiles_conf ]
then
  . $HOME/.dotfiles_conf
fi

if [ -f $HOME/.bash_aliases ]
then
  . $HOME/.bash_aliases
fi

if [ -f $HOME/.bash_aliases_ext ]
then
  . $HOME/.bash_aliases_ext
fi
