# Street Gastro Restaraunt Booking App

![homepage](static/images/street-gastro-homepage.png)

## About

The live website can be accessed by visiting this [link](#).

The website Street Gastro a comprehensive restaurant and table booking platform that aims to provide a seamless and enjoyable experience for both customers and restaurant staff. It will serve as an online hub for the restaurant, offering various functionalities to enhance the dining process and facilitate table reservations.

## User Experience Design

### Strategy

Build a user-friendly restaurant and table booking website using Django Allauth and Python. The website allows customers to browse the menu, make table reservations, and leave star ratins on indivudual dishes. Utilize Django's models and database relationships to ensure efficient data management.

### Target Audience

The target audience for the restaurant and table booking website includes both potential customers looking for a dining experience and restaurant staff or management responsible for handling table reservations. The website aims to cater to diners seeking convenient online table bookings and menu exploration while providing restaurant personnel with with a simple task manger for guest and tables booked.

### User Stories

#### Customer Goals

- As a customer I can see clear and attractive images of the dishes on the menu so that I can make better dining choices.
- As a customer I can filter the menu by dietary preferences so that I can find suitable options.
- As a customer I can reserve a table online with a simple and user-friendly booking system.
- As a customer I can receive an email confirmation so that my reservation is confirmed.
- As a customer I can edit or cancel my table reservation online so that can make changes if I need to.
- As a customer I can see star ratings from other diners so that I gauge the restaurant's quality.
- As a customer, I want the website to be mobile-responsive so that I book a table easily on my smartphone or tablet.

#### Manager and Staff Goals

- As a staff/manager member I can have access to the table reservation task manager so that I can check how many guests and tables are booked for that day


## Technologies used
- ### Languages:
    + [Python](https://www.python.org/downloads/release/python-385/): the primary language used to develop the server-side of the website.
    + [JS](https://www.javascript.com/): the primary language used to develop interactive components of the website.
    + [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML): the markup language used to create the website.
    + [CSS](https://developer.mozilla.org/en-US/docs/Web/css): the styling language used to style the website.
- ### Frameworks and libraries:
    + [Django](https://www.djangoproject.com/): python framework used to create all the backend logic of the website.
    + [jQuery](https://jquery.com/): was used to control click events and sending AJAX requests.
    + [jQuery User Interface](https://jqueryui.com/) was used to create interactive elements and animations.
    + [Django Channels](https://channels.readthedocs.io/en/latest/): was used to create real-time communication between users.
- ### Databases:
    + [Elephantsql](https://www.elephantsql.com/): the database used to store all data.


  
## Features

![hero section](static/images/home-hero-section.png)

**Hero Section**
- The user is welcomed by the ambieance of the restaraunt in the hero image. With clear call to action buttons to book a table or browse the menu dish images and see the star ratings for each dish.
  
![welcome section](static/images/welcome-section.png)

**Welcome Section**
- When scrolling down there is a nice and invitin welsome section. Withe a nice presentation about the restarant and elegant image of a dish.
  
![sample menu section](static/images/sample-menu-section.png)

**Sample Menu Section**
- When scrolling further the user is presented with to sample dishes and description from the menu.
  
![booking section](static/images/booking-section.png)

**Booking Section**
- when scrolling the user is preneted with a beautifull booking section.
- Clear call to action to book a table.
- Booking form with name, email, geusts, date. 
- Book button, edit button and cancel button. 

![gallery section](static/images/rotating-gallery.png)

**Gallery Section**
- Scroll further and the user is presented with a roatating gallery. also a prenetation on the ethos of Street gastro and localy sourced produce.

![menu](static/images/menu.png)

**Interactive Menu**
- The website will showcase an interactive and visually appealing menu, displaying dishes with high-quality images and detailed descriptions. 
- Customers can easily filter through the menu to explore various food options.
- The customer can also rate dishes with a 1 - 5 star rating. view the average rating for each dish.

**Mobile Responsiveness**
- The website will be fully responsive to different devices, including smartphones and tablets, allowing customers to access it on the go.

**Reservation Confirmation and Reminders**
- After booking a table, customers will receive instant confirmation via email. Additionally.

**Staff Management Interface**
- The website will provide atask manager for restaurant staff to see how many guests and tables are booked for that day.

**Overall**
- The website will serve as an efficient and user-friendly platform, streamlining the table booking process for customers and providing restaurant staff with tools to manage reservations effectively. 
- The goal is to create a positive and convenient dining experience that encourages repeat visits and word-of-mouth recommendations.

## Information Architecture

### Database

- During the earliest stages of the project, the database was created using ElephantSQL.

### Data Modeling

**Relationship diagram**

![Relationship diagram](static/images/relational-diagram.png)

1. **Allauth User Model**
    - The user model was created using [Django-allauth](https://django-allauth.readthedocs.io/en/latest/).
    - The user model was then migrated to PostgreSQL.

2. **Customer User Model**

![Customer user model](static/images/customer-user-model.png)

3. **Staff Member User Model**

![Staff member user model](static/images/staff-user-model.png)


## Design


### Color Scheme

- The color scheme of the application is based on the dark black, greens and light green colors:

![Color Scheme](static/images/color-palette.png)

- The decision to use this color palette was made to give it a natural warm restaurant feel.

### Typography

The main font used in the website is Gruppo. The use of this font is consistent with style and elegance of the restaraunt. Needless to say, the Gruppo font was chosen due to its readability, which increases user experience.

  ![Typography](static/images/gruppo-font.png)


### Imagery

- The main background image waswas found at pexels.com [BGJar](https://www.pexels.com). All other images was found on pexels or my own personal images.

### Wireframes ###

**Home**

![Home](static/images/wireframe-home.jpg)

**Menu**

![Menu](static/images/wireframe-menu.jpg)

**Book**

![Book](static/images/wireframe-book.jpg)

**Contact**

![Contact](static/images/wireframe-contact.jpg)



