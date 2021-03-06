from client import *
from copy import copy, deepcopy
import Queue as Q
import random
from math import *
from sets import Set
import time


MANHATAN_CACHE = [[[None for k in xrange(100)] for j in xrange(10)] for i in xrange(10)]

class Player(object):
    Taquin = [[]]

    def __init__( self , url="http://localhost:8080" , size = 2 , pid = 1 , name="DCD" , oid = 1):
        self.url = url
        self.size = int( size )
        self.Taquin = \
                  [ [ 0 for i in range( self.size ) ] \
                    for j in range( self.size ) ]
        print self.Taquin
        self.pid = pid
        self.name = name
        self.oid = oid #id del oponente
    """
        constructor para jugar solo 
    """
    def __init__( self , url="http://localhost:8080" , size = 2 , pid = 1 , name="DCD" , oid = 1 , Taquin  = [[]] , i = 0 , j = 0):
        self.url = url
        self.size = int( size )
        self.Taquin = \
                  [ [ 0 for w in range( self.size ) ] \
                    for z in range( self.size ) ]
        self.pid = pid
        self.name = name
        self.oid = oid #id del oponente
        self.Taquin = Taquin
        self.i = i 
        self.j = j
        print self.Taquin
        self.Taquin[ i ][ j ] = None
        self.TaquinCopy = deepcopy( Taquin )


    def get_challenge( self ):
        challenge = get_board( self.url , self.pid )
        self.size = len( challenge["currentState"] ) 
        print "el tam del reto es de %i" % self.size
        self.Taquin = \
                  [ [ 0 for i in range( self.size ) ] \
                    for j in range( self.size ) ]
        for i in range( len( challenge["currentState"] ) ):
             for j in range( len( challenge["currentState"] ) ):
                            try:
                                self.Taquin[ i ][ j ] = int( challenge["currentState"][ i ][ j ] )
                            except:
                                print "error al parsear %s" % challenge["currentState"][ i ][ j ]
                                self.Taquin[ i ][ j ]  = None
        self.i = int( challenge["blank"]["row"] )
        self.j = int( challenge["blank"]["column"] )
        self.Taquin[ self.i ][ self.j ] = None
        self.print_taquin()

    def compete( self ):
        raw_input( " Oprime enter una vez te hallan retado" ) 
        self.get_challenge( )
        self.simulate_player( )
        
    def initialize_ordered_matrix( self ):
        count = 1
        for i in range( self.size ):
            for j in range( self.size ):
                self.Taquin[ i ][ j ] = count
                count = count + 1
        self.Taquin[ self.size - 1 ][ self.size - 1] = None
        self.i = self.size - 1
        self.j = self.size - 1

     
    def add_challenge( self , Matrix , i , j  ):
        challenge( self.url , Matrix , i , j , self.oid )

    def shuffle( self ):
        moves = []
        for k in range( self.size + 5 ):
            move = self.random_move(  )
            moves.append( move )
            #raw_input("Press Enter to continue...")
            self.move( move , False )   
        return moves
            
    def get_valid_moves( self ):
        valid_moves = []
        if self.i > 0:
            valid_moves.append( 2 )
        if self.i < self.size - 1:
            valid_moves.append( 3 )
        if self.j > 0:
            valid_moves.append( 1 )
        if self.j < self.size - 1:
            valid_moves.append( 0 )
        random.shuffle( valid_moves )
        return valid_moves

    def random_move( self ):
        moves = self.get_valid_moves()
        return moves[ random.randint( 0 , len( moves ) - 1 ) ]

    def register( self ):
        create_player( self.url , self.pid , self.name )

    def challenge( self ):
        """ por ahora el challenge es retar con lo que tambien me pusieron """
        print "Se va a hacer un chalenge de %i %i" % ( self.i , self.j )
        challenge( self.url , self.Taquin , self.i , self.j , self.oid )

    def create_player( self ):
        generateBoard( self.url , self.Taquin , self.i , self.j )
        self.register( )

    def swap( self , initial_i , initial_j , end_i , end_j ):
        copy = self.Taquin[ initial_i ][ initial_j ]
        self.Taquin[ initial_i ][ initial_j ] = self.Taquin[ end_i ][ end_j ]
        self.Taquin[ end_i ][ end_j ] = copy

    """
        funcion que mueve al jugador en la direccion direction, el segundo paramtero isCopy es para que las copias de jugadores no alteren el estado del servidor
        si isCopy es True, no envia nada al servidor
    """
    def move( self , direction , isCopy ):
        if direction == 0:
            if not isCopy:
                print "        Movimiento derecha %i %i" % ( self.i , self.j )
                move_right( self.url , self.pid )
            self.swap( self.i , self.j , self.i , self.j + 1 )
            self.j = self.j + 1
        elif direction == 1:
             if not isCopy:
                print "        Movimiento izquierda %i %i" % ( self.i , self.j )
                move_left( self.url , self.pid )
             self.swap( self.i , self.j , self.i , self.j - 1 )
             self.j = self.j - 1
        elif direction == 2:
            if not isCopy:
                print "         Movimiento arriba %i %i" % ( self.i , self.j )
                move_up( self.url , self.pid )
            self.swap( self.i , self.j , self.i - 1 , self.j )
            self.i = self.i - 1
        elif direction == 3:
            if not isCopy:
                print "         Movimiento abajo %i %i" % ( self.i , self.j )
                move_down( self.url , self.pid )
            self.swap( self.i , self.j , self.i + 1 , self.j )
            self.i = self.i + 1
        else:
             "Invalid Move!"
        if not isCopy:
            self.print_taquin()

    def is_ordered( self ):
        array = []
        count = 0
        for i in range( len( self.Taquin ) ):
            for j in range( len( self.Taquin ) ):
                array.append( self.Taquin[ i ][ j ] )
        current = deepcopy( array )
        array.sort()
        array.append( None ) # pongo uno extra para que el None quede al final
        array.pop( 0 )
        for k in range( len( array ) ):
            if array[ k ] != current[ k ]:
                return False
        return True

    def print_taquin( self ):
        print "********************************************"
        s = [[str(e) for e in row] for row in self.Taquin]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print '\n'.join(table)
        print "********************************************\n"

    def imprimir_movimiento( self,  movimiento ):
        """ derecha izq arr abajo"""
        if movimiento == 0:
            return "derecha"
        if movimiento == 1:
            return "izquierda"
        if movimiento == 2:
            return "Arriba"
        if movimiento == 3:
            return "Abajo"

    def simulate_player( self ): 
        print "*************** Jugador *************************"
        previous = None
        best = None
        movimientos = []
        estados = []
        total_movimientos = 0
        camino = ""
        start = time.time()
        queue = Q.PriorityQueue()
        best = None
        while best is None or best.exact_total_distance > 0 :
            moves = self.get_valid_moves()
            total_movimientos = total_movimientos + 1

            for movement in moves:
                player_copy = deepcopy( self )
                player_copy.move( movement , True )
                if best != None:
                    camino = best.path + str( movement )
                    total_movimientos = best.move_count + 1
                else:
                    camino = str( movement )
                    total_movimientos = 1
                move = Movement( player_copy.Taquin , player_copy.i , player_copy.j , movement , total_movimientos , camino , best )
                #aca falta es no crear siempre los movimietos completos si no solo llamar a las funciones de calculo si no lo he hecho antes
                if move not in estados:
                    queue.put( move )
                    estados.append( move )
                else:
                    for estado in estados:
                        if estado.is_equal( move ):
                            move.path = estado.path
            
            previous = deepcopy( best )
            best = queue.get( )
            print "     el mejor movimiento con distancia %f y direccion %s" % ( best.exact_total_distance , self.imprimir_movimiento( best.movement ) )
            self.Taquin = best.Taquin
            self.i = best.i 
            self.j = best.j
            movimientos.append( best )
            #raw_input("...")
            
        print "FIN! total movimientos=%i" % total_movimientos
        print "camino %s %i" % ( movimientos[ len( movimientos ) - 1 ].path, len( movimientos[ len( movimientos ) - 1 ].path ) )
        end = time.time()
        print "Se demoro %f" %(end - start)
        raw_input( "Termina")
        self.Taquin = self.TaquinCopy
        for move in  movimientos[ len( movimientos ) - 1 ].path :
            self.print_taquin()
            print "Se mueve %s i:%i j:%i" % ( move , self.i , self.j )
            self.move( int(move) , False )

                #if puedo llegar desde movimeinto a movimiento temp

                # verifico si puedo llegar al estado

            
            #print "El mejor movimiento es hacia %i %i " % ( best.i , best.j )



class Movement:

    def __init__( self, Taquin , i , j , movement , move_count , path , previous ):
        self.Taquin = deepcopy( Taquin )
        self.path = path
        self.previous = previous
        self.i = deepcopy( i )
        self.j = deepcopy( j )
        self.movement = deepcopy( movement )
        self.move_count = move_count
        self.correctly_placed = 0#self.count_correctly_placed()
        self.exact_total_distance = self.count_exact_total_distance()
        #print " Se crea un movimiento con puestos %i y distancia %i , movmiento %i y camino %s " % ( self.correctly_placed , self.exact_total_distance , movement, path)
        
        
        #print "Correctos %i - Distancia %f" % ( self.correctly_placed ,  self.exact_total_distance)


    def print_taquin( self ):
        print "********************************************"
        s = [[str(e) for e in row] for row in self.Taquin]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print '\n'.join(table)
        print "********************************************\n"

    def can_reach( self , other ):
        x_distance = abs(self.i - other.i)
        y_distance = abs(self.j - other.j)
        different = 0
        for i in range( len( self.Taquin ) ):
            for j in range( len( self.Taquin ) ):
                if self.Taquin[ i ][ j ] != other.Taquin[ i ][ j ]:
                    different = different + 1
        
        if different == 2 and x_distance + y_distance == 1:
            return True
        return False
 
    def count_exact_total_distance( self ):
        if self.previous is None:
            count = 0
            array = []
            total_distance = 0.0
            last = ( len( self.Taquin ) * len( self.Taquin ) )
            for i in range( len( self.Taquin ) ):
                for j in range( len( self.Taquin ) ):
                    count = count + 1
                    value = self.Taquin[ i ][ j ]
                    if value is not None:
                        distance = self.get_position_distance( self.Taquin[ i ][ j ] , i , j  )
                        total_distance = total_distance + distance
        else:
            # tengo que determinar cual ficha es necesario recalcular
            previous_i = self.previous.i
            previous_j = self.previous.j
            distance = self.previous.exact_total_distance - self.get_position_distance( self.Taquin[ previous_i ][ previous_j ] , self.i , self.j )
            distance += self.get_position_distance( self.Taquin[ previous_i ][ previous_j ] , previous_i , previous_j )
            current_row = 0

            for i in range( len( self.Taquin ) ):
                error = 0
                for j in range( len( self.Taquin ) ):
                    value = self.Taquin[ i ][ j ]
                    if value is not None:
                        mi_row = value / len( self.Taquin )
                        if mi_row == current_row and self.get_position_distance( value , i , j ) != 0:
                            error += 1
                if error > 1:
                    distance += error - 1
                current_row += 1



                current_row += 1
            #self.print_taquin()
            #raw_input("Distancia con cache %i " % distance )
            # ahora hace falta el conflicto lineal

            return distance
        return total_distance

    def get_position_distance( self , number , i , j ):
        if MANHATAN_CACHE[ i ][ j ][ number ] != None:
            return MANHATAN_CACHE[ i ][ j ][ number ]
        count = 0
        i_r = 0
        j_r = 0
        for x in range( len( self.Taquin ) ):
            for y in range( len( self.Taquin ) ):
                count = count + 1
                if count == number:
                    #print "En %i %i va %i " %( x , y , number )
                    i_r = x
                    j_r = y

        #distancia euclideana
        # en i_r y j_r el lugar en donde deberia ir la ficha
        MANHATAN_CACHE[ i ][ j ][ number ] = abs( i - i_r ) + abs( j_r - j )
        return  abs( i - i_r ) + abs( j_r - j )



    def count_correctly_placed( self ):
        array = []
        count = 0
        for i in range( len( self.Taquin ) ):
            for j in range( len( self.Taquin ) ):
                array.append( self.Taquin[ i ][ j ] )
        current = deepcopy( array )
        array.sort()
        array.append( None ) # pongo uno extra para empezar desde 1
        array.pop( 0 )
        for k in range( len( array ) ):
            if array[ k ] == current[ k ]:
                count = count + 1
        return count

    def is_equal( self , other ):
        if other == None:
            #raw_input("Uno de ellos es None")
            return False
        if self.i != other.i or self.j != other.j:
            return False

        for i in range( len( self.Taquin ) ):
            for j in range( len( self.Taquin ) ):
                if self.Taquin[ i ][ j ] != other.Taquin[ i ][ j ]:
                    #raw_input("NO SON IGUALES")
                    return False
        #raw_input("SON IGUALES")
        return True


    def __eq__( self , other ):
        if other == None:
            return False    
        for i in range( len( self.Taquin ) ):
            for j in range( len( self.Taquin ) ):
                if self.Taquin[ i ][ j ] != other.Taquin[ i ][ j ]:
                    #raw_input("NO SON IGUALES")
                    return False
        #raw_input("SON IGUALES")
        return True

    def __cmp__( self , other ):
        if other == None:
            return 1
        first =  cmp( self.exact_total_distance**2 + self.move_count , other.exact_total_distance**2 + other.move_count ) 

        if first != 0:
           return first
        return -1 * cmp( self.correctly_placed  , other.correctly_placed ) 




 
    


