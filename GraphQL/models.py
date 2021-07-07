from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import backref, relationship

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    name = Column(String)

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Use default=func.now() para definir o tempo de contratação padrão
    # de um funcionário para ser a hora atual quando um registro de funcionário for criado
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    # Use cascade='delete,all' para propagar a exclusão de um departamento para seus funcionários
    department = relationship(
        Department,
        backref=backref('employees',
                        uselist=True,
                        cascade='delete,all'))
    role = relationship(
        Role,
        backref=backref('roles',
                        uselist=True,
                        cascade='delete,all'))

# Importando tudo que é necessário
# >>> from database import engine, db_session
# >>> from models import Base, Department, Employee
# >>> Base.metadata.create_all(bind=engine)

# Preenchendo as tabelas com dados
# >>> engenharia = Department(name='Engenharia')
# >>> db_session.add(engenharia)
# >>> rh = Department(name='Recursos Humanos')
# >>> db_session.add(rh)
# >>> gabriel = Employee(name='Gabriel', department=engenharia)
# >>> db_session.add(gabriel)
# >>> rafael = Employee(name='Rafael', department=engenharia)
# >>> db_session.add(rafael)
# >>> maria = Employee(name='Maria', department=rh)
# >>> db_session.add(maria)
# >>> db_session.commit()