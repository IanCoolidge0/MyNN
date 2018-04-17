from mygrad.linalg import einsum
from mygrad import add

from mynn.initializers.uniform import uniform
from mynn.initializers.constant import constant

class dense:
    ''' A fully-connected layer.

    This class will perform a dense (fully-connected) linear operation on an (N, D)-shape
    input tensor with a (D, M)-shape weight tensor and a (M,)-shape bias.
    
    Parameters
    ----------
    input_size : int
        The number of features for each input datum.

    output_size : int
        The number of output units (neurons).

    weight_initializer : Callable, optional (default=initializers.uniform)
        The function to use to initialize the weight matrix.

    bias_initializer : Callable, optional (default=initializers.constant)
        The function to use to initialize the bias vector.

    weight_kwargs : dictionary, optional (default={})
        The keyword arguments to pass to the weight initialization function.

    bias_kwargs : dictionary, optional (default={})
        The keyword arguments to pass to the bias initialization function.
    '''
    def __init__(self, input_size, output_size, *, weight_initializer=uniform,
                 bias_initializer=constant, weight_kwargs={}, bias_kwargs={}):
        self.weight = weight_initializer(input_size, output_size, **weight_kwargs)
        self.bias = bias_initializer(1, output_size, **bias_kwargs)
        self.bias.data = self.bias.data.astype(self.weight.dtype)
        self.training = True

    def __call__(self, x):
        ''' Perform the forward-pass of the densely-connected layer over `x`.

        Parameters
        ----------
        x : Union[numpy.ndarray, mygrad.Tensor], shape=(N, D)
            The input to pass through the layer.

        Returns
        -------
        mygrad.Tensor
            The result of applying the dense layer wx + b.
        '''
        return add(einsum('ij,jk', x, self.weight, constant=(not self.training)),
                   self.bias, constant=(not self.training))

    @property
    def parameters(self):
        ''' Access the parameters of the model.

        Returns
        -------
        Tuple[mygrad.Tensor, mygrad.Tensor]
            The weight and bias of this layer.
        '''
        return (self.weight, self.bias)