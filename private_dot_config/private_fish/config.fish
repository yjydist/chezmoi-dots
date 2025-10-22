if status is-interactive
    # Commands to run in interactive sessions can go here
end

set -U fish_greeting

set -gx http_proxy 127.0.0.1:10808
set -gx https_proxy 127.0.0.1:10808
set -gx PATH /opt/homebrew/bin \
	~/.cargo/bin \
	$PATH

alias ls 'eza -l --icons --no-user --no-filesize'
alias mc macchina
alias ff fastfetch
