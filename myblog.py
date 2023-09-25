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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1145, debug=True, threaded=True)
