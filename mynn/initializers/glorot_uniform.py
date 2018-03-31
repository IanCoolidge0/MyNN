import numpy as np
from mygrad import Tensor

def glorot_uniform(shape=(3, 3)):
    ''' Initialize a :class:`mygrad.Tensor` according to the uniform initialization procedure
    described by Glorot and Bengio.

    Parameters
    ----------
    shape : Tuple[int, ..., int], optional (default=(3, 3))
        The shape of the output Tensor. Note that `shape` must be at least two-dimensional.

    Returns
    -------
    mygrad.Tensor, shape=`shape`
        A Tensor, with values initialized according to the glorot uniform initialization.

    Extended Description
    --------------------
    Glorot and Bengio put forward this initialization in the paper
        "Understanding the Difficulty of Training Deep Feedforward Neural Networks"
    http://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf

    A Tensor :math:`W` initialized in this way should be drawn from a distribution about

    .. math::
        U[-\frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}}, \frac{\sqrt{6}}{\sqrt{n_j+n_{j+1}}}]
    '''
    assert len(shape) >= 2, 'Glorot Uniform initialization requires at least two dimensions!'

    tensor = np.empty(shape)
    gain = 1
    bound = gain * np.sqrt(6 / ((shape[0] + shape[1]) * tensor[0, 0].size))
    return Tensor(np.random.uniform(-bound, bound, shape))
