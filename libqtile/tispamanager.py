import dbus
from manager import Qtile
import gobject
from libqtile.command import lazy
import os

class Tispa(Qtile):
    def __init__(self, config,
                 displayName=None, fname=None, no_spawn=False, log=None,
                 state=None):
        Qtile.__init__(self, config, displayName, fname, no_spawn, log, state)
    
    def loop(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        
        bus = dbus.SessionBus()
        controller = Controller(bus, self)
        
        self.server.start()
        timer = gobject.timeout_add(100, self.keepalive)
        self.log.info('Adding io watch')
        display_tag = gobject.io_add_watch(
            self.conn.conn.get_file_descriptor(),
            gobject.IO_IN, self._xpoll)
        try:
            context = gobject.main_context_default()
            while True:
                if context.iteration(True):
                    try:
                        # this seems to be crucial part
                        self.conn.flush()

                    # Catch some bad X exceptions. Since X is event based, race
                    # conditions can occur almost anywhere in the code. For
                    # example, if a window is created and then immediately
                    # destroyed (before the event handler is evoked), when the
                    # event handler tries to examine the window properties, it
                    # will throw a BadWindow exception. We can essentially
                    # ignore it, since the window is already dead and we've got
                    # another event in the queue notifying us to clean it up.
                    except (xcb.xproto.BadWindow, xcb.xproto.BadAccess):
                        # TODO: add some logging for this?
                        pass
                if self._exit:
                    self.log.info('Got shutdown, Breaking main loop cleanly')
                    break
                if self._abort:
                    self.log.warn('Got exception, Breaking main loop')
                    sys.exit(2)
        finally:
            self.log.info('Removing source')
            gobject.source_remove(display_tag)
            gobject.source_remove(timer)
            
    def keepalive(self):
        pass

class Controller(dbus.service.Object):
    def __init__(self, session, manager):
        dbus.service.Object.__init__(self, dbus.service.BusName('de.trollhoehle.tispa', session), '/')
        self.manager = manager
    
    @dbus.service.method('de.trollhoehle.tispa')
    def blub(self):
        return "Hello World!"
    
    @dbus.service.method('de.trollhoehle.tispa')
    def killTop(self):
        return self.manager.currentLayout.killTop()
       
    @dbus.service.method(dbus_interface='de.trollhoehle.tispa', in_signature='i')
    def setReplace(self,num):
        return self.manager.currentLayout.setToReplace(num)
        
    @dbus.service.method(dbus_interface='de.trollhoehle.tispa', in_signature='i')
    def toFullscreen(self, num):
        return self.manager.currentLayout.toFullscreen(num)
        
    @dbus.service.method('de.trollhoehle.tispa')
    def endFullscreen(self):
        return self.manager.currentLayout.endFullscreen()
    
    @dbus.service.method(dbus_interface='de.trollhoehle.tispa', in_signature='ii')
    def setColsRows(self, cols, rows):
        return self.manager.currentLayout.setColsRows(cols,rows)
        
