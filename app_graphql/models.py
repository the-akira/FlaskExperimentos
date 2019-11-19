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
    # Use default=func.now() to set the default hiring time
    # of an Employee to be the current time when an
    # Employee record was created
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
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

# >>> from models import engine, db_session, Base, Department, Employee
# >>> Base.metadata.create_all(bind=engine)

# >>> # Fill the tables with some data
# >>> engineering = Department(name='Engineering')
# >>> db_session.add(engineering)
# >>> hr = Department(name='Human Resources')
# >>> db_session.add(hr)

# >>> peter = Employee(name='Peter', department=engineering)
# >>> db_session.add(peter)
# >>> roy = Employee(name='Roy', department=engineering)
# >>> db_session.add(roy)
# >>> tracy = Employee(name='Tracy', department=hr)
# >>> db_session.add(tracy)
# >>> db_session.commit()