def concatenate_color_lists(object fcls):
    cdef ColorMatrix result
    cdef ColorMatrix source

    result = ColorMatrix()
    for fcl in fcls:
        source = toColorMatrix(fcl)
        result.thisptr.extend(source.thisptr[0])
    return result
