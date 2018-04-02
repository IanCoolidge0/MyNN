from mygrad.operations import Operation
from mygrad import Tensor
import numpy as np

class FocalLoss(Operation):
    ''' Returns the focal loss as described in https://arxiv.org/abs/1708.02002 which is
    given by -ɑ(1-p)ˠlog(p).

    Extended Description
    --------------------
    The focal loss is given by

    .. math::
        \frac{1}{N}\sum\limits_{1}^{N}-\alpha_i(1-p_i)^\gamma\log(p_i)

    where :math:`N` is the number of elements in `x` and `y`.
    '''
    def __call__(self, outputs, targets, alpha, gamma):
        '''
        Parameters
        ----------
        outputs : mygrad.Tensor, shape=(N, C)
            The C class scores for each of the N pieces of data.

        targets : Union[mygrad.Tensor, Sequence[int]], shape=(N,)
            The correct class indices, in [0, C), for each datum.

        alpha : Real
            The ɑ weighting factor in the loss formulation.

        gamma : Real
            The ɣ focusing parameter.

        Returns
        -------
        numpy.ndarray
            The average focal loss.
        '''
        if isinstance(targets, Tensor):
            targets = targets.data

        self.variables = (outputs,)
        scores = np.copy(outputs.data)
        max_scores = np.max(scores, axis=1, keepdims=True)
        np.exp(scores - max_scores, out=scores)
        scores /= np.sum(scores, axis=1, keepdims=True)
        label_locs = (range(len(scores)), targets)
        correct_scores = scores[label_locs]

        loss = -np.mean(alpha * (1-correct_scores)**gamma * np.log(correct_scores))

        self.back = scores
        self.back[label_locs] += (1 - correct_scores)**gamma * (gamma * correct_scores *
                                                                np.log(correct_scores) - 1)
        self.back /= scores.shape[0]
        return loss
    
    def backward_var(self, grad, index, **kwargs):
        self.variables[index].backward(grad * self.back, **kwargs)

def focal_loss(x, y, alpha=1, gamma=0):
    '''
    Parameters
    ----------
    outputs : mygrad.Tensor, shape=(N, C)
        The C class scores for each of the N pieces of data.

    targets : Sequence[int], shape=(N,)
        The correct class indices, in [0, C), for each datum.

    alpha : Real, optional (default=1)
        The ɑ weighting factor in the loss formulation.

    gamma : Real, optional (default=0)
        The ɣ focusing parameter. Note that for Ɣ=0 and ɑ=1, this is cross-entropy loss.

    Returns
    -------
    numpy.ndarray
        The average focal loss.
    '''
    return Tensor._op(FocalLoss, x, op_args=(y, alpha, gamma))
