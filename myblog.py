# -*- encoding: utf-8 -*-
from typing import *
from app import app, db

from app.models import *


@app.shell_context_processor
def relate_shell_context() -> Dict[str, Any]:
    """
    when executing shells under current pwd,
    this func relates the shell context to db, app instances
    |> flask shell
    """
    return {
        'app': app,
        'db': db,
        'BlogUser': BlogUser,
        'Posts': Posts,
    }


app.run(host='127.0.0.1', port=5000, debug=True)
