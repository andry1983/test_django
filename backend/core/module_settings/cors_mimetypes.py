from backend.helpers.env_args import env

# cors
if env('DJANGO_DEBUG'):
    # PORT this is port for the frontend devServer
    port = env('PORT')
    protocol = env('DJANGO_DEFAULT_HTTP_PROTOCOL')
    CORS_ORIGIN_WHITELIST = [f'{protocol}://{host}:{port}'
                             for host in env('DJANGO_CORS_ORIGIN_WHITELIST')]

    import mimetypes

    mimetypes.add_type('application/javascript', '.js', True)
    mimetypes.add_type('text/css', '.css')
    mimetypes.add_type('text/javascript', '.js')
