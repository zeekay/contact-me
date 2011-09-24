#!/usr/bin/env python2
import os, select, socket, sys, time

print 'Connecting to chat...'
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect(('irc.freenode.net', 6667))
irc.send('NICK %s\r\n' % os.getlogin())
irc.send('USER so irc.freenode.net bla :so\r\n')

print 'Connecting to chat...'
irc.send('PRIVMSG zk :hello!\r\n')

while True:
    read, write, error = select.select([sys.stdin, irc],[],[])
    for i in read:
        if i == sys.stdin:
            irc.send('PRIVMSG zk :%s\r\n' % i.readline())
            sys.stdout.write('> ')
            sys.stdout.flush()
        elif i == irc:
            buffer = i.recv(1024)
            for line in buffer.splitlines():
                try:
                    _, info, line = line.split(':', 2)
                except ValueError: break
                if 'PRIVMSG' in info:
                    sys.stdout.write('\x08'*2)
                    sys.stdout.write('< %s\n> ' % line)
                    sys.stdout.flush()
    time.sleep(0.01)
