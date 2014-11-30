cdef extern from "echomesh/audio/DefaultDevice.h" namespace "echomesh::audio":
    double defaultInputSampleRate()
    double defaultOutputSampleRate()
    string defaultOutputDevice()
    string defaultInputDevice()
    vector[string] getDeviceNames(bool wantInputs)

def default_output_device():
    return defaultOutputDevice()

def default_input_device():
    return defaultInputDevice()

def default_output_sample_rate():
    return defaultOutputSampleRate()

def get_device_names(bool want_inputs):
    return getDeviceNames(want_inputs)
