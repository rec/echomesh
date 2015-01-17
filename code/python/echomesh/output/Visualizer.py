from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.base import Settings
from echomesh.expression import Expression
from echomesh.output.Poll import Poll
from echomesh.util.settings.SettingsValues import SettingsValues
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Visualizer(Poll):
    INSTANCE = None

    def __init__(self, **values):
        if not Visualizer.INSTANCE:
            Visualizer.INSTANCE = self

        self.values = SettingsValues(
          settings={
            'brightness': 'light.brightness',
            'instrument_padding': 'light.visualizer.instrument.padding',
            'label_padding': 'light.visualizer.instrument.label_padding',
            'label_starts_at_zero':
              'light.visualizer.instrument.label_starts_at_zero',
            'layout': 'light.visualizer.layout',
            'light_count': 'light.count',
            'padding': 'light.visualizer.padding',
            'period': 'light.visualizer.period',
            'show_label': 'light.visualizer.instrument.label',
            'shape': 'light.visualizer.instrument.shape',
            'size': 'light.visualizer.instrument.size',
            'transform': 'light.visualizer.transform',
            },
          values=values,
          update_callback=self.update_callback)

        assert cechomesh.is_started()
        self.lighting_window = cechomesh.PyLightingWindow()
        super(Visualizer, self).__init__(is_redirect=False)
        self.values.add_client()

    def _close_window(self):
        self.lighting_window = None

    def pause(self):
        super(Visualizer, self).pause()
        self._close_window()

    def snapshot(self, filename):
        self.lighting_window.save_snapshot_to_file(filename)

    def update_callback(self):
        self.period = Expression.convert(self.values.period)
        self.lighting_window.set_light_count(
          self.values.light_count or (
              self.values.layout[0] * self.values.layout[1]))
        self.lighting_window.set_shape(self.values.shape == 'rect')
        self.lighting_window.set_show_label(self.values.show_label)
        self.lighting_window.set_label_starts_at_zero(
          self.values.label_starts_at_zero)
        self.lighting_window.set_layout(
          self.values.layout, self.values.size, self.values.padding,
          self.values.instrument_padding, self.values.label_padding)
        self.columns = self.values.layout[0]

        self.transform = self.values.transform
        if self.transform:
            try:
                self.transform = cechomesh.Transform(self.transform)
            except:
                LOGGER.error('Don\'t understand transform %s', self.transform)
                self.transform = None
        self.brightness = Expression.convert(self.values.brightness)
        if self.transform:
            self.brightness = self.transform.apply(self.brightness)

    def emit_output(self, data):
        lights = cechomesh.combine_color_lists(data)
        lights.columns = self.columns
        lights.scale(self.brightness)
        self.lighting_window.set_lights(lights)

def instance():
    if not Visualizer.INSTANCE:
        Visualizer()
    return Visualizer.INSTANCE

def set_visible(visible):
    if visible or Visualizer.INSTANCE:
        instance().lighting_window.visible = visible
