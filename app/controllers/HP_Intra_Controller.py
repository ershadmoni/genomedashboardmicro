class HP_intra(object):
    """Data Structure for intra Helical parameters, including Shear, Stretch, Stagger, Buckle, Prop-Tw and Opening."""

    def __init__(self, she, str, sta, buc, pro, ope):
        self.she = she
        self.str = str
        self.sta = sta
        self.buc = buc
        self.pro = pro
        self.ope = ope
