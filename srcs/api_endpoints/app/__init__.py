from flask import Flask

def create_app():
    app = Flask(__name__)

    # register blueprints
    from .routes.ingest_routes import ingest_bp
    from .routes.query_routes import query_bp

    app.register_blueprint(ingest_bp, url_prefix="/api")
    app.register_blueprint(query_bp, url_prefix="/api")

    # initialize DB (create table if missing)
    from .db.vector_store import VectorStore
    VectorStore().initialize()

    return app
