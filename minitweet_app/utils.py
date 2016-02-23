def redirect_back(default='home'):
    return request.args.get('next') or \
        request.referrer or \
        url_for(default)
