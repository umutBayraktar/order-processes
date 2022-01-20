# order-processes

# Getting Started 

    We have three subprojects:
    order-accept : Accept orders and write to queue
    order-commit : Comsumes queue and write to database
    order-list : Read to database and represents and API
    
  All projects have setup documentation represented in their own paths. You can run them on your local machines. But you should set up the first order-list subproject because database migrations are in this project.
