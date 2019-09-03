from flask_restplus import Namespace, Resource, fields, reqparse

from models.employee import EmployeeModel
from models.used_hardware import UsedHardwareModel


FIRST_NAME_TEXT = 'Employee first name.'
SECOND_NAME_TEXT = 'Employee second name.'
USERNAME_TEXT = 'Employee username.'

api = Namespace('employees', description='Employees related operations')

employee = api.model('Employee', {
    'id': fields.Integer(required=True, description='Employee identifier'),
    'first_name': fields.String(required=True, description=FIRST_NAME_TEXT),
    'second_name': fields.String(required=True, description=SECOND_NAME_TEXT),
    'username': fields.String(required=True, description=USERNAME_TEXT)
})

parser = reqparse.RequestParser()
parser.add_argument('first_name', help=FIRST_NAME_TEXT)
parser.add_argument('second_name', help=SECOND_NAME_TEXT)
parser.add_argument('username', help=USERNAME_TEXT)

parser_required = reqparse.RequestParser()
parser_required.add_argument('first_name', required=True, help=FIRST_NAME_TEXT)
parser_required.add_argument('second_name', required=True, help=SECOND_NAME_TEXT)
parser_required.add_argument('username', required=True, help=USERNAME_TEXT)


@api.route('/', methods=['GET', 'POST'])
class EmployeesList(Resource):
    @api.marshal_list_with(employee)
    def get(self):
        """List all employees"""
        employees = EmployeeModel.get_all()
        return employees

    @api.doc(responses={400: 'Employee already exist',
                        500: 'Failed to add'})
    @api.marshal_list_with(employee)
    @api.expect(parser_required)
    def post(self):
        """Add new employee"""
        data = parser_required.parse_args()
        username = data['username']

        if EmployeeModel.find_by_username(username) is not None:
            api.abort(400, f'Employee {username} already exist')

        employee = EmployeeModel(**data)
        try:
            employee.save_employee()
        except:
            api.abort(500, 'Failed to add new employee')

        return employee


@api.route('/<employee_id>', methods=['GET', 'DELETE', 'PUT'])
@api.param('employee_id', 'Employee identifier')
@api.doc(responses={404: 'Employee does not exist'})
class Employee(Resource):

    @staticmethod
    @api.marshal_with(employee)
    def get(employee_id):
        """Fetch an employee given its identifier"""
        employee = EmployeeModel.find_by_id(employee_id)
        if employee is not None:
            return employee
        api.abort(404, f'Employee {employee_id} does not exist')

    @staticmethod
    @api.marshal_list_with(employee)
    def delete(employee_id):
        """Delete employee"""
        employee = EmployeeModel.find_by_id(employee_id)
        used_hardware = UsedHardwareModel.find_by_employee_id(employee_id)

        # First unlink all hardware, then delete
        if used_hardware:
            UsedHardwareModel.delete_links(employee_id)

        if employee is not None:
            employee.delete_employee()
            return employee
        api.abort(404, f'Employee {employee_id} does not exist')

    @staticmethod
    @api.doc(responses={400: 'Incorrect parameters',
                        500: 'Failed to update'})
    @api.marshal_list_with(employee)
    @api.expect(parser)
    def put(employee_id):
        """Update employee"""
        data = parser.parse_args()
        first_name = data['first_name']
        second_name = data['second_name']
        username = data['username']

        if first_name is None and second_name is None and username is None:
            api.abort(400, 'You need to specify minimum one parameter')

        employee = EmployeeModel.find_by_id(employee_id)
        if employee is not None:
            if first_name is not None:
                employee.first_name = first_name
            if second_name is not None:
                employee.second_name = second_name
            if username is not None:
                if EmployeeModel.find_by_username(username) is not None:
                    api.abort(400, f'Employee {username} already exist')
                employee.username = username
            try:
                employee.save_employee()
            except:
                api.abort(500, 'Failed to update employee')
            return employee
        api.abort(404, f'Employee {employee_id} does not exist')
