"""
histogram_eq.py

"""

from core import table

MENU = "Fil&ter"
LABEL = "Equalize Histogram (Python)"
DESCRIPTION = "Equalize the histogram of this image."

def execute( width, height, data ):
    
    histogram_table = [ 0 ] * 256
    histogram_sum = [ 0 ] * 256

    intdata = [ ord( c ) for c in data ]


    # compute the histogram for the image
    for i in range( 0, len( intdata ), 3 ):
        histogram_table[ ( 1 + intdata[ i ] + intdata[ i+1 ] + intdata[ i+2 ] ) / 3 ] += 1
    
    # compute the sums of pixels
    pixelcount = width * height
    s = 0
    for i in range( 0, 255 ):
        s += histogram_table[ i ]
        histogram_sum[ i ] = s * 255 / pixelcount

    print histogram_sum
    
    #now that the sums are computed it's time
    #to equalize the histogram and assign pixels
    
    #for i in range( len( data ) ):
        #intdata[ i ] = histogram_sum[ intdata[ i ] ]
        

    #data = [ chr( min( i, 255 ) ) for i in intdata ]

    #data = "".join( data )

    #return ( width, height, data )

    return table( width, height, data, histogram_sum )
    
