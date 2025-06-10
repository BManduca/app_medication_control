from flask import render_template 

def init_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/status_code_403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/status_code_404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/status_code_500.html'), 500
