import numpy as np
import warnings

from src.utils import softmax


class NaiveBayes:
    """
    A Naive Bayes classifier for binary data.
    """

    def __init__(self, smoothing=1):
        """
        Args:
            smoothing: controls the smoothing behavior when computing p(x|y).
                If the word "jackpot" appears `k` times across all documents with
                label y=1, we will instead record `k + self.smoothing`. Then
                `p("jackpot" | y=1) = (k + self.smoothing) / Z`, where Z is a
                normalization constant that accounts for adding smoothing to
                all words.
        """
        self.smoothing = smoothing

    def predict(self, X):
        """
        Return the most probable label for each row x of X.
        You should not need to edit this function.
        """
        probs = self.predict_proba(X)
        return np.argmax(probs, axis=1)

    def predict_proba(self, X):
        """
        Using self.alpha and self.beta, compute the probability p(y | X[i, :])
            for each row X[i, :] of X.  While you will have used log
            probabilities internally, the returned array should be
            probabilities, not log probabilities.

        See equation (9) in `naive_bayes.pdf` for a convenient way to compute
            this using your self.alpha and self.beta. However, note that
            (9) produces unnormalized log probabilities; you will need to use
            your src.utils.softmax function to transform those into probabilities
            that sum to 1 in each row.

        Args:
            X: a sparse matrix of shape `[n_documents, vocab_size]` on which to
               predict p(y | x)

        Returns 
            probs: an array of shape `[n_documents, n_labels]` where probs[i, j] contains
                the probability `p(y=j | X[i, :])`. Thus, for a given row of this array,
                np.sum(probs[i, :]) == 1.
        """
        n_docs, vocab_size = X.shape
        n_labels = 2

        assert hasattr(self, "alpha") and hasattr(self, "beta"), "Model not fit!"
        assert vocab_size == self.vocab_size, "Vocab size mismatch"
       
        log_probs = np.zeros((n_docs, n_labels))
        for i in range(n_docs):
            for j in range(n_labels):
                log_probs[i, j] = self.alpha[j] + np.sum(X[i] * self.beta[:, j])
   
   
        probs = softmax(log_probs)
   
        return probs
     ##   raise NotImplementedError
    
        
    def fit(self, X, y):
        """
        Compute self.alpha and self.beta using the training data.
        You should store log probabilities to avoid underflow.
        This function *should not* use unlabeled data. Wherever y is NaN, that
        label and the corresponding row of X should be ignored.

        See equations (10) and (11) in `naive_bayes.pdf` for the math necessary
            to compute your alpha and beta.

        self.alpha should be set to contain the marginal probability of each class label.
        
        self.beta should be set to the conditional probability of each word
            given the class label: p(w_j | y_i). This should be an array of shape
            [n_vocab, n_labels].  Remember to use `self.smoothing` to smooth word counts!
            See __init__ for details. If we see M total words across all N documents with
            label y=1, have a vocabulary size of V words, and see the word "jackpot" `k`
            times, then: `p("jackpot" | y=1) = (k + self.smoothing) / (M + self.smoothing *
            V)` Note that `p("jackpot" | y=1) + p("jackpot" | y=0)` will not sum to 1;
            instead, `sum_j p(word_j | y=1)` will sum to 1.

        Hint: when self.smoothing = 0, some elements of your beta will be -inf.
            If `X_{i, j} = 0` and `\beta_{j, y_i} = -inf`, your code should
            compute `X_{i, j} \beta_{j, y_i} = 0` even though numpy will by
            default compute `0 * -inf` as `nan`.

            This behavior is important to pass both `test_smoothing` and
            `test_tiny_dataset_a` simultaneously.

            The easy way to do this is to leave `X` as a *sparse array*, which
            will solve the problem for you. You can also explicitly define the
            desired behavior, or use `np.nonzero(X)` to only consider nonzero
            elements of X.

        Args: X, a sparse matrix of word counts; Y, an array of labels
        Returns: None; sets self.alpha and self.beta
        """
        n_docs, vocab_size = X.shape
        n_labels = 2
        self.vocab_size = vocab_size
        B = X.toarray()
        print("X=",X)
        print("y=",y)
    ##    print("docs = ",n_docs)
     ##   print("size = ",vocab_size)
        print("smoothing=",self.smoothing)
        T1 = X.toarray()
        T2 = X.nonzero()
        sum1 = 0
        sum2 = 0
        for i in range(0, n_docs):
            if np.isnan(y[i]):
                continue
            if y[i] == 0:
                sum1= sum1+1
            else:
                sum2=sum2+1
        sum1 = sum1/n_docs
        sum2 = sum2/n_docs
        self.alpha = np.zeros(2)
        self.alpha[0] = np.log(sum1)
        self.alpha[1] = np.log(sum2)
        
        self.beta =np.zeros((vocab_size,n_labels))
        ### bj,0
        b0=0
        b1 =0
        for j in range(0,vocab_size):
            
         
            for i in range(0, n_docs):
                if np.isnan(y[i]):
                    continue
                if(y[i] ==0):
                    b0+= B[i][j]
                   
                else:
                  b1 += B[i][j]
                  
                  
        for j in range(0,vocab_size):
            up0= 0
            up1 = 0
            
            for i in range(0, n_docs):
                if np.isnan(y[i]):
                    continue
                if(y[i] ==0):
                  up0+= B[i][j]
                   
                else:
                  up1 += B[i][j]
            
            self.beta[j][0] = np.log((up0+self.smoothing)/(b0+self.smoothing*vocab_size))
            
            self.beta[j][1] = np.log((up1+self.smoothing)/(b1+self.smoothing*vocab_size))
       ## print("alpha = ",self.alpha)
       ## print("beta=",self.beta)
        ##   raise NotImplementedError
      
        
        
        
        

    def likelihood(self, X, y):
        r"""
        Using fit self.alpha and self.beta, compute the log likelihood of the data.
            You should use logs to avoid underflow.
            This function should not use unlabeled data. Wherever y is NaN,
            that label and the corresponding row of X should be ignored.

        Equation (5) in `naive_bayes.pdf` contains the likelihood, which can be written:

            \sum_{i=1}^N \alpha_{y_i} + \sum_{i=1}^N \sum_{j=1}^V X_{i, j} \beta_{j, y_i}

            You can visualize this formula in http://latex2png.com

        Args: X, a sparse matrix of word counts; Y, an array of labels
        Returns: the log likelihood of the data
        """
        assert hasattr(self, "alpha") and hasattr(self, "beta"), "Model not fit!"

        n_docs, vocab_size = X.shape
        n_labels = 2
        
        B = X.toarray()
      
        '''
        mask = ~np.isnan(y)
        X = X[mask]
        y = y[mask].astype(int)
        print(self.alpha)
        print(self.beta)
    # Compute log likelihood using Equation (5)
        print("sum1 =",self.alpha[y].sum())
        print("sum2=",self.beta[:, y].sum())
        sum2 = self.beta[:, y].sum()
##        for i in range(0,sum2.shape[0]):
  ##          for j in range(0,sum2.)
        log_likelihood = (self.alpha[y].sum() +
                      (X @ self.beta[:, y]).sum())
        print("sum3=",(X@self.beta[:, y]).sum())
        print("hood=",log_likelihood)
        return log_likelihood
        '''
        '''
        log_likelihood = 0.0
        for i in range(n_docs):
            if not np.isnan(y[i]):
                label = int(y[i])
                log_likelihood += np.log(self.alpha[label])
                for j in range(vocab_size):
                    count = X[i, j]
                    log_likelihood += count * np.log(self.beta[j, label])
        return log_likelihood
        '''
        B = X.toarray()
        likehood  = 0
        ayi = 0
        t = 0
        for i in range (0,n_docs):
            if np.isnan(y[i]):
                continue
            if y[i] == 0:
                ayi+=self.alpha[0]
            else:
                ayi+=self.alpha[1]
            for j in range(0,vocab_size):
               
                
                if y[i] == 0:
                    if np.isinf(self.beta[j][0]):
                        if B[i][j] == 0:
                            continue
                        else:
                            return -np.Inf
                    
                    t += B[i][j] * self.beta[j][0]
                else:
                    if np.isinf(self.beta[j][1]):
                        if B[i][j] == 0:
                            continue
                        else:
                            return -np.Inf
                        
                   
                    t += B[i][j] * self.beta[j][1]
        
        likehood = ayi+t
        return likehood