class Heuristic:
    def __init__(self, alpha=10, delta=(0.4, 2), beta=15):
        self.alpha = alpha
        self.delta = delta
        self.beta = beta
        self.analysis_type = None
        self.analysis_order = None
        self.description = None


class HeuristicSigma(Heuristic):
    def __init__(self, analysis_order='desc'):
        super(HeuristicSigma, self).__init__()
        self.analysis_order = analysis_order
        self.analysis_type = 'predicate'
        self.description = 'Sigma approach (JIDM) | most embracing predicate and most embracing facet'


class HeuristicPi(Heuristic):
    def __init__(self, analysis_order='asc'):
        super(HeuristicPi, self).__init__()
        self.analysis_order = analysis_order
        self.analysis_type = 'predicate'
        self.description = 'Pi approach (short paper) | most restrictive predicate and most embracing faceted'


class HeuristicOmega(Heuristic):
    def __init__(self, analysis_order='desc'):
        super(HeuristicOmega, self).__init__()
        self.analysis_order = analysis_order
        self.analysis_type = 'facet'
        self.description = 'Omega approach | most embracing facet, regardless the predicate'
