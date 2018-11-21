# Britecore Feature Request Application
A "feature request" is a request for a new feature that will be added onto an existing piece of software. Assume that the user is an employee at IWS who would be entering this information after having some correspondence with the client that is requesting the feature. The necessary fields are:

-   **Title:**  A short, descriptive name of the feature request.
-   **Description:**  A long description of the feature request.
-   **Client:**  A selection list of clients (use "Client A", "Client B", "Client C")
-   **Client Priority:**  A numbered priority according to the client (1...n). Client Priority numbers should not repeat for the given client, so if a priority is set on a new feature as "1", then all other feature requests for that client should be reordered.
-   **Target Date:**  The date that the client is hoping to have the feature.
-   **Product Area:**  A selection list of product areas (use 'Policies', 'Billing', 'Claims', 'Reports')


## Technology Stack:
- Python 2.7
- Flask
- SQLAlchemy
- JQuery


## Data Model:

    class Feature(db.Model):
        __tablename__ = 'features'
        id = db.Column(db.Integer(), primary_key=True)
        title = db.Column(db.String(255), nullable=False)
        description = db.Column(db.Text(), nullable=False)
        client = db.Column(String(50))
        priority = db.Column(Integer)
        target_date = db.Column(DateTime)
        product_area = db.Column(String(50)) 
        created_on = db.Column(db.DateTime(), default=datetime.utcnow)
        updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow) 


## Deployment:
Visit: [Deployment Guide for Flask on Heroku](https://github.com/datademofun/heroku-basic-flask)


### Author:
Bastin Robins .j - <bastinrobins@gmail.com>