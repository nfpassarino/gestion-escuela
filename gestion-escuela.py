import datetime
import csv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Time, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

#Conexión
engine = create_engine('sqlite:///:memory:')
Base = declarative_base(engine)

class Alumno(Base):
    __tablename__ = 'alumno'
    id = Column(Integer,Sequence('alumno_id_seq'), primary_key = True)
    nombre = Column(String)
    apellido = Column(String)
    curso_id = Column(Integer, ForeignKey('curso.id'))

    curso = relationship('Curso', back_populates = 'alumnos')

    def __repr__(self):
        return'{} {}'.format(self.nombre, self.apellido)

class Curso(Base):
    __tablename__ = 'curso'
    id = Column(Integer, Sequence('curso_id_seq'), primary_key = True)
    nombre = Column(String)

    alumnos = relationship('Alumno', order_by = 'Alumno.id', back_populates = 'curso')
    horario = relationship('Horario', order_by = 'Horario.hora_inicio', back_populates = 'curso')

    def __repr__(self):
        return'{} Alumnos: {}\n'.format(self.nombre, self.alumnos)

class Horario(Base):
    __tablename__ = 'horario'
    id = Column(Integer, Sequence('horario_id_seq'), primary_key = True)
    dia = Column(String)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    profesor_id = Column(Integer, ForeignKey('profesor.id'))
    curso_id = Column(Integer, ForeignKey('curso.id'))

    curso = relationship("Curso", back_populates = 'horario')
    profesor = relationship("Profesor", back_populates = 'horarios')

    def __repr__(self):
        return'{}: {} - {} hs'.format(self.dia, self.hora_inicio, self.hora_fin)

class Profesor(Base):
    __tablename__ = 'profesor'
    id = Column(Integer, Sequence('profesor_id_seq'), primary_key = True)
    nombre = Column(String)
    apellido = Column(String)

    horarios = relationship("Horario", back_populates = 'profesor')

    def __repr__(self):
        return'{} {}'.format(self.nombre, self.apellido)

class CursoLista(object):

    def __init__(self, path):
        self.path = path

    def export(self, curso):
        alumnos = curso.alumnos
        with open(self.path, 'w') as a_file:
            writer = csv.writer(a_file)
            for alum in alumnos:
                writer.writerow([str(alum)])


#Creación de la db
Base.metadata.create_all(engine)

#Creación de la sesión
Session = sessionmaker(bind = engine)
session = Session()

#Creación de cursos
c1 = Curso(nombre = 'Carpintería')
c2 = Curso(nombre = 'Bicicletería')
c3 = Curso(nombre = 'Jardinería')

#Creación de asignaturas
lunm = Horario(dia = 'Lunes', hora_inicio = datetime.time(10, 0, 0), hora_fin = datetime.time(12, 0, 0))
lunt = Horario(dia = 'Lunes', hora_inicio = datetime.time(16, 0, 0), hora_fin = datetime.time(18, 0, 0))
marm = Horario(dia = 'Martes', hora_inicio = datetime.time(10, 0, 0), hora_fin = datetime.time(12, 0, 0))
mart = Horario(dia = 'Martes', hora_inicio = datetime.time(16, 0, 0), hora_fin = datetime.time(18, 0, 0))
miem = Horario(dia = 'Miércoles', hora_inicio = datetime.time(10, 0, 0), hora_fin = datetime.time(12, 0, 0))
miet = Horario(dia = 'Miércoles', hora_inicio = datetime.time(16, 0, 0), hora_fin = datetime.time(18, 0, 0))
juem = Horario(dia = 'Jueves', hora_inicio = datetime.time(10, 0, 0), hora_fin = datetime.time(12, 0, 0))
juet = Horario(dia = 'Jueves', hora_inicio = datetime.time(10, 0, 0), hora_fin = datetime.time(18, 0, 0))
viem = Horario(dia = 'Viernes', hora_inicio = datetime.time(10, 0, 0), hora_fin = datetime.time(12, 0, 0))
viet = Horario(dia = 'Viernes', hora_inicio = datetime.time(16, 0, 0), hora_fin = datetime.time(18, 0, 0))
sabm = Horario(dia = 'Sábado', hora_inicio = datetime.time(10, 0, 0), hora_fin = datetime.time(12, 0, 0))
sabt = Horario(dia = 'Sábado', hora_inicio = datetime.time(16, 0, 0), hora_fin = datetime.time(18, 0, 0))
domm = Horario(dia = 'Domingo', hora_inicio = datetime.time(10, 0, 0), hora_fin = datetime.time(12, 0, 0))
domt = Horario(dia = 'Domingo', hora_inicio = datetime.time(16, 0, 0), hora_fin = datetime.time(18, 0, 0))

#Creación de profesores
p1 = Profesor(nombre = 'Alberto', apellido = 'Carpenter')
p2 = Profesor(nombre = 'Julia', apellido = 'Bicicecich')
p3 = Profesor(nombre = 'Daniela', apellido = 'Tomatovich')

#Asignaciones
c1.horario = [marm, juem, sabt]
c2.horario = [lunt, miet, viet]
c3.horario = [lunm, mart, miem, juet, viem, sabm]

p1.horarios.extend([marm, juem, sabt])
p2.horarios.extend([lunt, miet, viet])
p3.horarios.extend([lunm, mart, miem, juet, viem, sabm])

c1.alumnos=[Alumno(nombre = 'Franco', apellido = 'Fernandez'),
            Alumno(nombre = 'Martin', apellido = 'Perez'),
            Alumno(nombre = 'Tomás', apellido = 'Gonzalez'),
            Alumno(nombre = 'Cristian', apellido = 'Martinez')]

c2.alumnos=[Alumno(nombre = 'Elisa', apellido = 'Paez'),
            Alumno(nombre = 'Fernanda', apellido = 'García'),
            Alumno(nombre = 'Paula', apellido = 'Sosa'),
            Alumno(nombre = 'Gabriela', apellido = 'Gieco')]

c3.alumnos=[Alumno(nombre = 'Lautaro', apellido = 'Aznar'),
            Alumno(nombre = 'Walter', apellido = 'Spinetta'),
            Alumno(nombre = 'Vanina', apellido = 'Lebon'),
            Alumno(nombre = 'Noelia', apellido = 'Moro')]

#Persistencia
session.add(c1)
session.add(c2)
session.add(c3)
session.add(p1)
session.add(p2)
session.add(p3)
session.commit()

#Salida de datos
print('Desea visualizar:\n\t1. Alumnos por curso\n\t2. Horario de profesores\n\t3. Horario de cursos\n\t4. Exportar lista de alumnos por curso')
while True:
    op = input(':::::Ingrese una opcion: \n')
    if op.isdigit() and int(op) < 5 and int(op) > 0:
        if int(op) == 1:
            list_alum = session.query(Curso).all()
            for curso in list_alum:
                print(curso)
            break
        elif int(op) == 2:
            list_prof = session.query(Horario).all()
            for horario in list_prof:
                print('{}\t\t{}'.format(horario.profesor, horario))
            break
        elif int(op) == 3:
            list_cur = session.query(Horario).all()
            for horario in list_cur:
                print('{}\t\t{}'.format(horario.curso.nombre, horario))
            break
        elif int(op) == 4:
            CursoLista('curso_{}.csv'.format(c1.nombre)).export(c1)
            CursoLista('curso_{}.csv'.format(c2.nombre)).export(c2)
            CursoLista('curso_{}.csv'.format(c3.nombre)).export(c3)
            break
    else:
        print(':::::Ingrese una opción válida (1, 2, 3 o 4):::::')