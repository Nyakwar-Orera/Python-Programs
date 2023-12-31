import warnings
import numpy as np

from src.utils import softmax, stable_log_sum
from src.naive_bayes import NaiveBayes


class NaiveBayesEM(NaiveBayes):
    """
    A NaiveBayes classifier for binary data, that uses both unlabeled and
        labeled data in the Expectation-Maximization algorithm

    Note that the class definition above indicates that this class
        inherits from the NaiveBayes class. This means it has the same
        functions as the NaiveBayes class unless they are re-defined in this
        function. In particular you should be able to call `self.predict_proba`
        using your implementation from `src/naive_bayes.py`.
    """

    def __init__(self, max_iter=10, smoothing=1):
        """
        Args:
            max_iter: the maximum number of iterations in the EM algorithm,
                where each iteration contains both an E step and M step.
                You should check for convergence after each iterations,
                e.g. with `np.isclose(prev_likelihood, likelihood)`, but
                should terminate after `max_iter` iterations regardless of
                convergence.
            smoothing: controls the smoothing behavior when computing p(x|y).
                If the word "jackpot" appears `k` times across all documents with
                label y=1, we will instead record `k + self.smoothing`. Then
                `p("jackpot" | y=1) = (k + self.smoothing) / Z`, where Z is a
                normalization constant that accounts for adding smoothing to
                all words.
        """
        self.max_iter = max_iter
        self.smoothing = smoothing

    def initialize_params(self, vocab_size, n_labels):
        """
        Initialize self.alpha such that
            `log p(y_i = k) = -log(n_labels)`
            for all k
        and initialize self.beta such that
            `log p(w_j | y_i = k) = -log(vocab_size)`
            for all j, k.

        """
        self.alpha = -np.log(n_labels) * np.ones(n_labels)
        self.beta = -np.log(vocab_size) * np.ones((vocab_size, n_labels))

    def fit(self, X, y):
        """
        Compute self.alpha and self.beta using the training data.
        You should store log probabilities to avoid underflow.
        This function *should* use unlabeled data within the EM algorithm.

        During the E-step, use the NaiveBayes superclass self.predict_proba to
            infer a distribution over the labels for the unlabeled examples.
            Note: you should *NOT* replace the true labels with your predicted
            labels. You can use a `np.where` statement to only update the
            labels where `np.isnan(y)` is True.

        During the M-step, update self.alpha and self.beta, similar to the
            `fit()` call from the NaiveBayes superclass. However, when counting
            words in an unlabeled example to compute p(x | y), instead of the
            binary label y you should use p(y | x).

        For help understanding the EM algorithm, refer to the lectures and
            the handout. In particular, Figure 2 shows the algorithm for
            semi-supervised Naive Bayes.

        self.alpha should contain the marginal probability of each class label.

        self.beta should contain the conditional probability of each word
            given the class label: p(x | y). This should be an array of shape
            [n_vocab, n_labels].  Remember to use `self.smoothing` to smooth word counts!
            See __init__ for details. If we see M total
            words across all documents with label y=1, have a vocabulary size
            of V words, and see the word "jackpot" `k` times, then:
            `p("jackpot" | y=1) = (k + self.smoothing) / (M + self.smoothing * V)`
            Note that `p("jackpot" | y=1) + p("jackpot" | y=0)` will not sum to 1;
            instead, `sum_j p(word_j | y=1)` will sum to 1.

        Note: if self.max_iter is 0, your function should call
            `self.initialize_params` and then break. In each
            iteration, you should complete both an E-step and
            an M-step.

        Args: X, a sparse matrix of word counts; Y, an array of labels
        Returns: None
        """
        n_docs, vocab_size = X.shape
        n_labels = 2
        self.vocab_size = vocab_size
        
        self.initialize_params(vocab_size, n_labels)
        
        prev_likelihood = 0
        for i in range(self.max_iter):
            # E-step
            prob_label = self.predict_proba(X)
            # print(self.alpha,self.beta)
            # print(prob_label)
            # Update labels for unlabeled data
            y_pred = np.where(np.isnan(y), prob_label[:,1], y)
            # print(y_pred)
            # M-step
            # Update alpha
            self.alpha[0] = np.log(np.sum(1-y_pred)/np.sum(1-y))
            self.alpha[1] = np.log(np.sum(y_pred)/np.sum(y))
            # Update beta
            # Count words in each class
            total_words_in_class = np.zeros((n_labels, vocab_size))
            for j in range(n_docs):
                for v in range(vocab_size):
                    if X[j,v] > 0:
                        total_words_in_class[int(y_pred[j]), v] += X[j,v]
            # Update beta
            # print(total_words_in_class)
            # print(np.sum(total_words_in_class, axis=1))
            for k in range(n_labels):
                for v in range(vocab_size):
                    # print(v,k)
                    # print(total_words_in_class[k,v], np.sum(total_words_in_class[k,:]) + self.smoothing * vocab_size)
                    self.beta[v,k] = np.log((total_words_in_class[k,v] + self.smoothing) / (np.sum(total_words_in_class[k,:]) + self.smoothing * vocab_size))
            # Compute log likelihood
            likelihood = self.likelihood(X, y)
            # print(f'Iteration {i}: likelihood {likelihood}')
            # Check convergence
            if np.isclose(prev_likelihood, likelihood):
                break
            else:
                prev_likelihood = likelihood
        

    def likelihood(self, X, y):
        r"""
        Using fit self.alpha and self.beta, compute the likelihood of the data.
            This function *should* use unlabeled data.
            This likelihood is defined in equation (14) of `naive_bayes.pdf`.

        For unlabeled data, we predict `p(y_i = y' | X_i)` using the
            previously-learned p(x|y, beta) and p(y | alpha).
            For labeled data, we define `p(y_i = y' | X_i)` as
            1 if `y_i = y'` and 0 otherwise; this is because for labeled data,
            the probability that the ith example has label y_i is 1.

        Following equation (14) in the `naive_bayes.pdf` writeup, the log
            likelihood of the data after t iterations can be written as:

            \sum_{i=1}^N \log \sum_{y'=1}^2 \exp(
                \log p(y_i = y' | X_i, \alpha, \beta) + \alpha_{y'}
                + \sum_{j=1}^V X_{i, j} \beta_{j, y'})

            You can visualize this formula in http://latex2png.com

            The tricky aspect of this likelihood is that we are simultaneously
            computing $p(y_i = y' | X_i, \alpha^t, \beta^t)$ to predict a
            distribution over our latent variables (the unobserved $y_i$) while
            at the same time computing the probability of seeing such $y_i$
            using $p(y_i =y' | \alpha^t)$.

            Note: In implementing this equation, it will help to use your
                implementation of `stable_log_sum` to avoid underflow. See the
                documentation of that function for more details.

        Args: X, a sparse matrix of word counts; Y, an array of labels
        Returns: the log likelihood of the data.
        """

        assert hasattr(self, "alpha") and hasattr(self, "beta"), "Model not fit!"

        n_docs, vocab_size = X.shape
        n_labels = 2
        
        # Predict labels for unlabeled data
        prob_label = self.predict_proba(X)
        # Update labels for unlabeled data
        y_pred = np.where(np.isnan(y), prob_label[:,1], y)

        log_likelihood = 0

        for i in range(n_docs):
            # Compute log p(y_i = y' | X_i, alpha, beta)
            log_prob = np.log(prob_label[i,:]) + self.alpha
            # Compute the sum of Xi * beta
            log_prob += np.dot(X[i,:].toarray()[0], self.beta)
            # Compute log sum exp(log_prob)
            log_likelihood += stable_log_sum(log_prob)
        
        return log_likelihood