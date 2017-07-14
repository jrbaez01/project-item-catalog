from item_catalog.db import DBSession
from item_catalog.models import User, Category, Item

categories = [
        ('Frontend',),
        ('Backend',),
        ('Non-Tech',),
        ('Dev Essentials',),
    ]

items = [
    (1, 1, "Front End Frameworks", "Explore and build interactive, single-page\
            applications with popular JavaScript frameworks! IN COLLABORATION\
            WITH Google"),
    (1, 1, "Intro to JavaScript", "Learn the fundamentals of JavaScript,\
            the most popular programming language in web development."),
    (1, 1, "Intro to HTML and CSS", "Learn how to convert digital design\
            mockups into static web pages and how to build a responsive\
            portfolio site to showcase your work."),
    (1, 2, "Intro to Relational Databases", "Relational databases are a\
            powerful tool used throughout the industry. Learn the basics of\
            SQL and how to connect your Python code\
            to a relational database."),
    (1, 2, "Full Stack Foundations", "Learn the fundamentals of back-end web\
            development by creating your own web application from the ground\
            up using the iterative development process."),
    (1, 2, "Authentication & Authorization: OAuth", "Learn to implement the\
            OAuth 2.0 framework to allow users to securely and easily login to\
            your web applications."),
    (1, 3, "App Monetization", "Learn how to effectively develop, implement,\
            and measure your monetization strategy, iterating on the model as\
            appropriate."),
    (1, 3, "Rapid Prototyping", "Learning to prototype will save you time and\
            money in the development process. You will create quality apps\
            faster and have confidence in the viability of your products."),
    (1, 3, "Intro to Psychology", "Go on a journey through psychological\
            concepts and principles to enable you to gain a more in-depth\
            understanding of human thought and behavior. IN COLLABORATION WITH\
            San Jose State Universit"),
    (1, 4, "Writing READMEs", "Documentation is an important part of the\
            development process. Learn to write READMEs using Markdown so your\
            code can be used by other humans!"),
    (1, 4, "Linux Command Line Basics", "An introduction to the Linux\
            command line interface."),
    (1, 4, "Version Control with Git", "Learn how to use Git, a popular\
            Version Control System and essential tool for any developer."),
    (1, 3, "First User", "The first registered user will be the owner of\
            of the item entries already created."),
]

for cat in categories:
    DBSession.add(Category(name=cat[0]))

for i in items:
    DBSession.add(Item(user_id=i[0], category_id=i[1], name=i[2], desc=i[3]))

DBSession.commit()
