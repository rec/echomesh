def concatenate_color_lists(object fcls):
    cdef ColorList result
    cdef ColorList source

    result = ColorList()
    for fcl in fcls:
        source = toColorList(fcl)
        result.thisptr.extend(source.thisptr[0])
    return result
