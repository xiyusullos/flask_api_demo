from flask import Flask, json
from flask_restful import Api, Resource, marshal, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'development key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/test1'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

api = Api(app)

resource_fields = {
    'id': fields.String,
    'ms_sub_class': fields.String(attribute='MSSubClass'),
    'ms_zoning': fields.String(attribute='MSZoning'),
    'lot_frontage': fields.String(attribute='LotFrontage'),
}


class HousePrice(db.Model):
    __tablename__ = 'house_price'

    id = db.Column(db.Integer, primary_key=True)
    MSSubClass = db.Column(db.String(255), name='ms_sub_class')
    MSZoning = db.Column(db.String(255), name='ms_zoning')
    LotFrontage = db.Column(db.String(255), name='lot_frontage')

    def __str__(self):
        return f'id={self.id}, MSSubClass={self.MSSubClass}, MSZoning={self.MSZoning}, LotFrontage={self.LotFrontage}'


# db.create_all()

def import_data(filepath='train.csv'):
    with open(filepath, 'r') as f:
        # get the head column name
        line = f.readline().strip()
        heads = line.split(',')
        # print(heads)

        for line in f:
            fields = line.strip().split(',')
            id_ = fields[0]
            MSSubClass = fields[1]
            MSZoning = fields[2]
            LotFrontage = fields[3]

            house_price = HousePrice(
                id=id_,
                MSSubClass=MSSubClass,
                MSZoning=MSZoning,
                LotFrontage=LotFrontage
            )
            db.session.add(house_price)
        db.session.commit()


create_parser = reqparse.RequestParser()
create_parser.add_argument('ms_sub_class', type=str, required=True)
create_parser.add_argument('ms_zoning', type=str, required=True)
create_parser.add_argument('lot_frontage', type=str, required=True)

update_parser = reqparse.RequestParser()
update_parser.add_argument('ms_sub_class', type=str, required=False)
update_parser.add_argument('ms_zoning', type=str, required=False)
update_parser.add_argument('lot_frontage', type=str, required=False)


class HousePriceResourceList(Resource):
    @marshal_with(resource_fields)
    def get(self):
        page_size = 10
        page = 1
        results = HousePrice.query.limit(page_size).offset(page_size * (page - 1)).all()
        return results

    @marshal_with(resource_fields)
    def post(self):
        args = create_parser.parse_args()
        house_price = HousePrice(
            MSSubClass=args.get('ms_sub_class'),
            MSZoning=args.get('ms_zoning'),
            LotFrontage=args.get('lot_frontage'),
        )
        db.session.add(house_price)
        db.session.commit()

        return house_price


class HousePriceResourceDetail(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        result = HousePrice.query.get_or_404(id)
        return result

    @marshal_with(resource_fields)
    def delete(self, id):
        result = HousePrice.query.get_or_404(id)
        db.session.delete(result)
        db.session.commit()

        return

    @marshal_with(resource_fields)
    def patch(self, id):
        args = update_parser.parse_args()
        result = HousePrice.query.get_or_404(id)

        fields = {
            'ms_sub_class': 'MSSubClass',
            'ms_zoning': 'MSZoning',
            'lot_frontage': 'LotFrontage',
        }
        for k in fields:
            if args.get(k, None) is not None:
                setattr(result, fields[k], args.get(k))

        db.session.add(result)
        db.session.commit()

        return result


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    api.add_resource(HousePriceResourceList, '/house_prices')
    api.add_resource(HousePriceResourceDetail, '/house_prices/<int:id>')

    # app.run(host='0.0.0.0', port=6000)
    app.run(debug=True)
