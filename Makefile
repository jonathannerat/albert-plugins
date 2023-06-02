TARGET = $(XDG_DATA_HOME)/albert
OPTS = --dotfiles -v -t $(TARGET)

install:
	stow $(OPTS) stow/

uninstall: OPTS += -D
uninstall: install

.PHONY = install uninstall
