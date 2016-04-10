
from system.core.router import routes



routes['default_controller'] = 'News'
routes['POST']['/search'] = 'News#search'
routes['/results'] = 'News#results'
routes['/paper/<id>'] = 'News#city_page'
routes['/new'] = 'News#new'
routes['POST']['/create'] = 'News#create'
routes['POST']['/login'] = 'News#login'
routes['/log_page'] = 'News#log_page'
routes['/dashboard/<double_id>'] = 'News#dashboard'
routes['POST']['/new_art'] = 'News#new_art'
routes['/dashboard/write/<init_c>'] = 'News#write_new'
routes['POST']['/write_submit'] = 'News#write_submit'
routes['POST']["/logout"] = 'News#logout'

    
    #routes['PUT']['/users/<int:id>'] = 'users#update'
    #routes['POST']['/users'] = 'users#create'
    #routes['GET']['/users/<int:id>'] = 'users#show'
    #routes['GET']['/users/<int:id>/edit' = 'users#edit'
    #routes['PATCH']['/users/<int:id>'] = 'users#update'
    #routes['DELETE']['/users/<int:id>'] = 'users#destroy'

