import math


def cdf(x):
    """Calculate approximation of Cumulative Distribution Function by using Hart Algorithms
            
        y = |x|
        
        if y < 7.07106781186547
            N(x) = exp(- y*y / 2) * (A / B)
            
            where
                A = (((((a1*y + a2)*y + a3)*y + a4)*y + a5)*y + a6)*y + a7
                B = ((((((b1*y + b2)*y + b3)*y + b4)*y + b5)*y + b6)*y + b7)*y + b8
            and
                a1 =   0.0352624965998911
                a2 =   0.700383064443688
                a3 =   6.37396220353165
                a4 =  33.912866078383
                a5 = 112.079291497871
                a6 = 221.213596169931
                a7 = 220.206867912376
                b1 =   0.0883883476483184
                b2 =   1.75566716318264
                b3 =  16.064177579207
                b4 =  86.7807322029461
                b5 = 296.564248779674
                b6 = 637.333633378831
                b7 = 793.826512519948
                b8 = 440.413735824752
                  
        if 37 >= y >= 7.07106781186547
            N(x) = exp(- y*y / 2) / (2.506628274631 * C)
            
            where
                C = y + 1 / (y + 2 / (y + 3 / (y + 4 / (y + 0.65))))
                
        if y > 37
            N(x) = 0
        
        When x > 0, N(x) = 1 - N(x)
    """

    y = math.fabs(x)

    if y < 7.07106781186547:
        a = (0.0352624965998911, 0.700383064443688,
             6.37396220353165,   33.912866078383,
             112.079291497871,   221.213596169931,
             220.206867912376
            )
        b = (0.0883883476483184, 1.75566716318264,
             16.064177579207,    86.7807322029461,
             296.564248779674,   637.333633378831,
             793.826512519948,   440.413735824752)

        aa = (((((a[0] * y + a[1]) * y + a[2]) * y + a[3]) * y + a[4]) * y + a[5]) * y + a[6]
        bb = ((((((b[0] * y + b[1]) * y + b[2]) * y + b[3]) * y + b[4]) * y + b[5]) * y + b[6]) * y + b[7]

        n = math.exp(- y * y / 2) * (aa / bb)

    elif 7.07106781186547 <= y <= 37:
        c = y + 1 / (y + 2 / (y + 3 / (y + 4 / (y + 0.65))))
        n = math.exp(- y * y / 2) / (2.506628274631 * c)

    else: # y > 37
        n = 0

    return (1 - n) if x > 0 else n


def norminv(p):
    """
    Modified from the author's original perl code (original comments follow below)
    by dfield@yahoo-inc.com.  May 3, 2004.

    Lower tail quantile for standard normal distribution function.

    This function returns an approximation of the inverse cumulative
    standard normal distribution function.  I.e., given P, it returns
    an approximation to the X satisfying P = Pr{Z <= X} where Z is a
    random variable from the standard normal distribution.

    The algorithm uses a minimax approximation by rational functions
    and the result has a relative error whose absolute value is less
    than 1.15e-9.

    Author:      Peter John Acklam
    Time-stamp:  2000-07-19 18:26:14
    E-mail:      pjacklam@online.no
    WWW URL:     http://home.online.no/~pjacklam
    """

    if p <= 0 or p >= 1:
        # The original perl code exits here, we'll throw an exception instead
        raise ValueError( "Argument %f must be in open interval (0,1)" % p )

    # Coefficients in rational approximations.
    a = (-3.969683028665376e+01,  2.209460984245205e+02,
         -2.759285104469687e+02,  1.383577518672690e+02,
         -3.066479806614716e+01,  2.506628277459239e+00)
    b = (-5.447609879822406e+01,  1.615858368580409e+02,
         -1.556989798598866e+02,  6.680131188771972e+01,
         -1.328068155288572e+01 )
    c = (-7.784894002430293e-03, -3.223964580411365e-01,
         -2.400758277161838e+00, -2.549732539343734e+00,
          4.374664141464968e+00,  2.938163982698783e+00)
    d = ( 7.784695709041462e-03,  3.224671290700398e-01,
          2.445134137142996e+00,  3.754408661907416e+00)

    # Define break-points.
    plow  = 0.02425
    phigh = 1 - plow

    if p < plow: # Rational approximation for lower region
        q = math.sqrt(-2*math.log(p))
        ret = (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    elif p > phigh: # Rational approximation for upper region
        q = math.sqrt(-2*math.log(1-p))
        ret = -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    else: # plow <= p <= phigh # Rational approximation for central region
        q = p - 0.5
        r = q*q
        ret = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)

    return ret