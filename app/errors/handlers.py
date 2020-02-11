from flask import render_template, jsonify
from app.errors import errors

@errors.app_errorhandler(400)
def bad_request(e):
    return jsonify({'message': e.description['message']}), 400

@errors.app_errorhandler(403)
def page_not_found(e):
    return render_template("errors/403.html"), 403

@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"), 404
    
@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500