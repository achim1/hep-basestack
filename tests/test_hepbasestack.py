import pytest

from hepbasestack import logger, itools, timeit, isnotebook, colors, layout

# helper functions generating test data
# provide a list of input/output

@pytest.fixture(params = [(([],0),[]),\
                          (([],1),[]),\
                          (([1,2],2),([1],[2])),\
                          (([1,2,3],2),([1,2],[3])),\
                          (([1,2,3],4), ([1],[2],[3],[])),\
                          (([1,2,3,4],2), ([1,2],[3,4]))])
def prepare_test_data_for_slicer(request):
    return request.param

@pytest.fixture(params = [(10,0),\
                          (20,0),\
                          (30,0)])
def prepare_test_data_for_logger(request):
    return request.param



# test itools    
def test_slicer(prepare_test_data_for_slicer):
    (func_args, desired_result) = prepare_test_data_for_slicer
    result = [r for r in itools.slicer(*func_args)]
    if len(result) == 1:
        result = result[0]
    elif len(result) > 1:
        result = tuple(result)
        
    assert result == desired_result

# test logger
def test_logger(prepare_test_data_for_logger):
    import logging

    loglevel, __ = prepare_test_data_for_logger
    assert isinstance(logger.get_logger(loglevel), logging.Logger)

def test_timit():
    @timeit 
    def sleeper():
        import time
        time.sleep(2)

    sleeper()

def test_isnotebook():
    assert (isnotebook() == False)

def test_flatten():
    data = [[1,3,4],[5,6,7],[8,9,10]]
    flattened = itools.flatten(data)
    assert flattened.ndim == 1
    assert len(flattened) == 9

def test_colors():
    cdict = colors.ColorDict()
    # the sole feature of ColorDict is 
    # to not raise a key error when a key 
    # is not known but return it instead
    assert cdict['idonotknowthiskey'] == 'idonotknowthiskey'

    palette = colors.get_color_palette()
    # there is a 'prohibited' color
    assert palette['prohibited'] != 'prohibited'
    assert len(palette.keys()) > 9
