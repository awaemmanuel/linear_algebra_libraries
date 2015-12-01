from math import acos, pi, sqrt
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR = 'Cannot normalize the zero vector'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'No Unique Orthogonal components'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No Unique Parallel components'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'Only defined in 2 or 3 dimensions'
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates
    
    
    def __add__(self, v):
        return Vector([round((x + y), 3) for x, y in zip(self.coordinates, v.coordinates)])
    
    def __sub__(self, v):
        return Vector([round((x - y), 3) for x, y in zip(self.coordinates, v.coordinates)])
    
    def scalar_multiply(self, c):
        #new_coordinates = [Decimal(c) * x for x in self.coordinates]
        return Vector([round((Decimal(c) * x), 3) for x in self.coordinates])
    
    def dot(self, v):
        return sum([round(x * y, 3) for (x, y) in zip(self.coordinates, v.coordinates)])
    
    
    def angle_between(self, v, in_degrees = False):
        try:
            x = self.normalize()
            y = v.normalize()
            angle_in_radians = acos(x.dot(y))
            
            if in_degrees:
                return angle_in_radians * (180. / pi)
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR:
                raise Exception('Cannot comput an angle with zero vectors')
     
    
    def magnitude(self):
        return round(sqrt(sum(map(lambda x: x ** 2, self.coordinates))), 3)
    
    def normalize(self):
        try:
        
            magnitude = self.magnitude()
            return self.scalar_multiply(Decimal('1.0') / Decimal(magnitude))

        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR)
    
    def is_zero(self, error_tolerance = 1e-10):
        return self.magnitude() < tolerance
    
    '''
        Orthogonality Check: If the dot product of two vectors is 0 or less than some tolerance
    '''
    def is_orthogonal_to(self, v, error_tolerance = 1e-10):
        return abs(self.dot(v)) < tolerance
    
    '''
        Parallel check if vectors are 0 vectors or if angle between them
        are 0 or 180
    '''
    def is_parallel_to(self, v):
        return ( self.is_zero() or 
                v.is_zero() or 
                self.angle_between(v) == 0 or 
                self.angle_between(v) == pi )
    
    '''
        Find component that's orthogonal to a vector
    '''
    def component_orthogonal_to(self, basis):
        try:
            proj = self.component_parallel_to(basis)
            return (self - projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e
                
    '''
        Find component that's parallel to a vector
    '''
    def component_parallel_to(self, basis):
        try:
            u = basis.normalize()
            weight = self.dot(u)
            return u.scalar_multiply(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e
    
    '''
        Cross product of two matrices
    '''
    def cross(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            return Vector([y_1*z_2 - y_2*z_1, -(x_1*z_2 - z_2*z_1), x_1*y_2 - x_2*y_1])
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or 
                 msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e
                
    '''
        Find area of a triangle bounded by two vectors
    '''
    def area_of_triangle_bounded_by(self, v):
        return self.aread_of_parallelogram_bounded_by(v) / Decimal('2.0')
    
    
    '''
        Find area of a parallelogram bounded by two vectors
    '''
    def aread_of_parallelogram_bounded_by(self, v):
        return self.cross(v).magnitude()
    
    
if __name__ == '__main__':
    a = Vector([8.218, -9.341])
    b = Vector([-1.129, 2.111])
    
    c = Vector([7.119, 8.215])
    d = Vector([-8.223, 0.878])
    
    e = Vector([1.671, -1.012, -0.318])
    f = 7.41
    
    g = Vector([-0.221, 7.437])
    h = Vector([8.813, -1.331, -6.247])
    
    i = Vector([5.581, -2.136])
    j = Vector([1.996, 3.108, -4.554])
    
    
#    print a + b
#    print c - d
#    print e.scalar_multiply(f)
    
    print "MAGNITUDES"
    print g.magnitude()
    print h.magnitude()
    
    print "NORMALIZATIONS"
    print i.normalize()
    print j.normalize()
    
    print "CROSS"
    v = Vector(['8.462', '7.893', '-8.187'])
    w = Vector(['6.984', '-5.975', '4.778'])
    print '#1: ', v.cross(w)
    