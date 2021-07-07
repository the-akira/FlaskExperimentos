from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """
    Importe todos os módulos aqui que possam definir modelos 
    para que sejam registrados corretamente nos metadados.
    Caso contrário, você terá que importá-los antes de chamar init_db()
    """
    from models import Department, Employee, Role
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Cria as fixtures
    engenharia = Department(name='Engenharia')
    db_session.add(engenharia)
    rh = Department(name='Recursos Humanos')
    db_session.add(rh)

    gerente = Role(name='gerente')
    db_session.add(gerente)
    engenheiro = Role(name='engenheiro')
    db_session.add(engenheiro)

    gabriel = Employee(name='Gabriel', department=engenharia, role=engenheiro)
    db_session.add(gabriel)
    rafael = Employee(name='Rafael', department=engenharia, role=engenheiro)
    db_session.add(rafael)
    maria = Employee(name='Maria', department=rh, role=gerente)
    db_session.add(maria)
    db_session.commit()