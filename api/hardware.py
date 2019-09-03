from flask_restplus import Namespace, Resource, fields, reqparse

from models.employee import EmployeeModel
from models.hardware import HardwareModel
from models.used_hardware import UsedHardwareModel


NAME_TEXT = 'Hardware name.'
CATEGORY_TEXT = 'Hardware category.'
HARDWARE_ID_TEXT = 'Hardware identifier.'
EMPLOYEE_ID_TEXT = 'Employee identifier.'

api = Namespace('hardware', description='Hardware related operations')

hardware_list = api.model('Hardware', {
    'id': fields.Integer(required=True, description=HARDWARE_ID_TEXT),
    'name': fields.String(required=True, description=NAME_TEXT),
    'category': fields.String(required=True, description=CATEGORY_TEXT),
})

used_hardware_list = api.model('UsedHardware', {
    'hardware_id': fields.Integer(required=True, description=HARDWARE_ID_TEXT),
    'employee_id': fields.Integer(required=True, description=EMPLOYEE_ID_TEXT),
})

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help=NAME_TEXT)
parser.add_argument('category', required=True, help=CATEGORY_TEXT)

parser_used = reqparse.RequestParser()
parser_used.add_argument('employee_id', required=True, help=EMPLOYEE_ID_TEXT)


@api.route('/', methods=['GET', 'POST'])
class HardwareList(Resource):
    @staticmethod
    @api.marshal_list_with(hardware_list)
    def get():
        """List all hardware"""
        hardware = HardwareModel.get_all()
        return hardware

    @staticmethod
    @api.doc(responses={500: 'Failed to add'})
    @api.marshal_list_with(hardware_list)
    @api.expect(parser)
    def post():
        """Add new hardware"""
        data = parser.parse_args()
        hardware = HardwareModel(**data)
        try:
            hardware.save_hardware()
        except:
            api.abort(500, 'Failed to add new hardware')

        return hardware


@api.route('/<hardware_id>', methods=['GET', 'DELETE'])
@api.param('hardware_id', 'Hardware identifier')
@api.doc(responses={404: 'Hardware does not exist'})
class Hardware(Resource):

    @staticmethod
    @api.marshal_with(hardware_list)
    def get(hardware_id):
        """Fetch a hardware given its identifier"""
        hardware = HardwareModel.find_by_id(hardware_id)
        if hardware is not None:
            return hardware
        api.abort(404, f'Hardware {hardware_id} does not exist')

    @staticmethod
    @api.marshal_list_with(hardware_list)
    def delete(hardware_id):
        """Delete hardware"""
        hardware = HardwareModel.find_by_id(hardware_id)
        used_hardware = UsedHardwareModel.find_by_hardware_id(hardware_id)

        # First unlink, then delete
        if used_hardware is not None:
            used_hardware.delete_link()

        if hardware is not None:
            hardware.delete_hardware()
            return hardware
        api.abort(404, f'Hardware {hardware_id} does not exist')


@api.route('/<hardware_id>/used', methods=['GET', 'POST', 'DELETE', 'PUT'])
@api.param('hardware_id', 'Hardware identifier')
class UsedHardware(Resource):
    @staticmethod
    @api.doc(responses={404: 'Hardware is not in use'})
    @api.marshal_list_with(used_hardware_list)
    def get(hardware_id):
        """Get used hardware"""
        hardware = UsedHardwareModel.find_by_hardware_id(hardware_id)
        if hardware is not None:
            return hardware
        api.abort(404, f'Hardware {hardware_id} is not in use')

    @staticmethod
    @api.doc(responses={400: 'Incorrect parameters',
                        500: 'Failed to link'})
    @api.marshal_list_with(used_hardware_list)
    @api.expect(parser_used)
    def post(hardware_id):
        """Link hardware with employee"""
        data = parser_used.parse_args()
        data['hardware_id'] = hardware_id
        employee_id = data['employee_id']

        if HardwareModel.find_by_id(hardware_id) is None:
            api.abort(400, f'Hardware {hardware_id} does not exist')

        if EmployeeModel.find_by_id(employee_id) is None:
            api.abort(400, f'Employee {employee_id} does not exist')

        if UsedHardwareModel.find_by_hardware_id(hardware_id) is not None:
            api.abort(400, f'Hardware {hardware_id} already in use')

        hardware = UsedHardwareModel(**data)
        try:
            hardware.save_link()
        except:
            api.abort(500, 'Failed to link hardware')

        return hardware

    @staticmethod
    @api.doc(responses={404: 'Hardware does not exist'})
    @api.marshal_list_with(used_hardware_list)
    def delete(hardware_id):
        """Unlink hardware"""
        hardware = UsedHardwareModel.find_by_hardware_id(hardware_id)
        if hardware is not None:
            hardware.delete_link()
            return hardware
        api.abort(404, f'Hardware {hardware_id} does not exist')

    @staticmethod
    @api.doc(responses={400: 'Incorrect parameters',
                        500: 'Failed to update'})
    @api.marshal_list_with(used_hardware_list)
    @api.expect(parser_used)
    def put(hardware_id):
        """Update employee linked to hardware"""
        data = parser_used.parse_args()
        employee_id = data['employee_id']

        employee = EmployeeModel.find_by_id(employee_id)
        if employee is None:
            api.abort(400, f'Employee {employee_id} does not exist')

        hardware = UsedHardwareModel.find_by_hardware_id(hardware_id)
        if hardware is not None:
            hardware.employee_id = employee_id
            try:
                hardware.save_link()
            except:
                api.abort(500, 'Failed to update employee')
            return hardware
        api.abort(400, f'Hardware {hardware_id} is not in use and cannot by modified')
