from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphene import relay
import graphene
from models import Department as DepartmentModel
from models import Employee as EmployeeModel
from models import Role as RoleModel

class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel
        interfaces = (relay.Node,)

class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel
        interfaces = (relay.Node,)

class Role(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel
        interfaces = (relay.Node,)

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Permitir apenas ordenação de coluna única
    all_employees = SQLAlchemyConnectionField(Employee, sort=Employee.sort_argument())
    # Permite a ordenação em várias colunas, por padrão na chave primária
    all_roles = SQLAlchemyConnectionField(Role)
    # Desativa a ordenação neste campo
    all_departments = SQLAlchemyConnectionField(Department, sort=None)

schema = graphene.Schema(query=Query, types=[Department, Employee, Role])